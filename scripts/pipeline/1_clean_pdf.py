import csv
import difflib
import hashlib
import os
import re
import shutil
import unicodedata
from tqdm import tqdm

import pymupdf
import requests
from crossref.restful import Works

#paths
pdf_raw_dir = "data/papers_test/pdf_raw"
pdf_clean_dir = "data/papers_test/pdf_clean"
rename_map = "data/papers_test/rename_map.csv"  # 1 line per raw PDF: raw_name, clean_name, doi, method, note

#setup
doi_regex = r'\b10\.\d{4,9}/[-.;()/:\w]+'
n_pages = 2          # own DOI and title are on the first pages; later pages hold DOIs of cited papers
n_hits = 5           # Crossref title-search results checked per query
min_match = 0.9      # title similarity needed to accept a Crossref record (OCR text has small errors)
works = Works()
fields = "DOI,title,author,issued,published-print,published-online"
map_header = ["raw_name", "clean_name", "doi", "method", "note"]


def find_doi(text):
    """First DOI in the text, without trailing punctuation."""
    found = re.findall(doi_regex, text)
    if not found:
        return None
    doi = found[0].rstrip(".,;:")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1].rstrip(".,;:")
    return doi


def page_text(page):
    """Text layer of a page; OCR (tesseract) when the page has none."""
    text = page.get_text()
    if not text.strip():
        text = page.get_text(textpage=page.get_textpage_ocr(dpi=300, full=True))
    return text


def largest_font_text(page):
    """Lines in the page's largest font: usually the title. Empty for pages without a text layer."""
    lines = [(span["size"], span["text"]) for block in page.get_text("dict")["blocks"]
             for line in block.get("lines", []) for span in line["spans"] if span["text"].strip()]
    if not lines:
        return ""
    top = max(size for size, _ in lines)
    return " ".join(text for size, text in lines if size >= 0.9 * top)


def ascii_name(text):
    """Family name safe for a file name: no accents, spaces or punctuation; 'BRADSTOCK' -> 'Bradstock'."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    if text.isupper():
        text = text.title()
    return re.sub(r"[^A-Za-z-]", "", text.replace(" ", "-"))


def squash(text):
    """Letters and digits only, for title matching; ligatures split ('ﬁ' -> 'fi')."""
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", text).lower())


def title_on_pages(title, text):
    """True if the title (first 60 letters) is printed in the text, allowing small OCR errors."""
    t, text = squash(title)[:60], squash(text)
    if len(t) < 15:
        return False
    if t in text:
        return True
    step = max(1, len(t) // 10)
    return any(difflib.SequenceMatcher(None, t, text[i:i + len(t)]).ratio() >= min_match
               for i in range(0, max(1, len(text) - len(t) + 1), step))


def year_of(metadata):
    """Publication year; 'created' is only the Crossref deposit date."""
    for key in ("issued", "published-print", "published-online"):
        parts = metadata.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return None


def name_from(metadata, text):
    """'Family_year' or 'Family_et_al_year' if the record is complete and its title is in the text; else (None, reason)."""
    authors = [a for a in metadata.get("author", []) if a.get("family")]
    year = year_of(metadata)
    title = (metadata.get("title") or [""])[0]
    if not authors or not year:
        return None, "Crossref record has no author or year"
    if not title_on_pages(title, text):
        return None, f"Crossref title not on first pages: {title[:80]}"
    family_name = ascii_name(authors[0]["family"])
    if len(authors) == 1:
        return f"{family_name}_{year}", ""
    return f"{family_name}_et_al_{year}", ""


def search_title(queries, text):
    """Crossref bibliographic search; first hit whose title is printed on the first pages."""
    for query in queries:
        try:
            #plain request: the crossref library pages with a cursor, which drops relevance ranking
            r = requests.get("https://api.crossref.org/works", timeout=30,
                             params={"query.bibliographic": query[:300], "rows": n_hits, "select": fields})
            r.raise_for_status()
            hits = r.json()["message"]["items"]
        except Exception as e:
            return None, None, f"Crossref error: {e}"
        for hit in hits:
            stem, _ = name_from(hit, text)
            if stem:
                return stem, hit["DOI"], ""
    return None, None, "no title-search hit matches the first pages"


def unique_name(stem, taken):
    """Add b, c, ... after the year when the name is already used."""
    name = f"{stem}.pdf"
    for letter in "bcdefghijklmnopqrstuvwxyz":
        if name not in taken:
            return name
        name = f"{stem}{letter}.pdf"
    raise RuntimeError(f"too many PDFs named {stem}")


#rename map from earlier runs: resume safe, never rename a PDF twice
#PDFs are moved, so pdf_raw holds only PDFs not yet named
#clean_name empty = no verified record: the PDF stays in pdf_raw for naming by hand
#method = manual: named by hand; the script never moves or deletes that PDF (rename and move it yourself)
rows = {}
if os.path.exists(rename_map):
    with open(rename_map, encoding="utf-8", newline="") as f:
        rows = {r["raw_name"]: r for r in csv.DictReader(f)}
taken = {r["clean_name"] for r in rows.values() if r["clean_name"]}


def same_file(a, b):
    """True if both files have the same bytes."""
    return hashlib.sha256(open(a, "rb").read()).digest() == hashlib.sha256(open(b, "rb").read()).digest()


def write_map():
    """Write the map after every PDF, so an interrupted run loses nothing."""
    with open(rename_map, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=map_header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows[k] for k in sorted(rows))


#rename pdfs
for pdf in tqdm(sorted(os.listdir(pdf_raw_dir))):
    if not pdf.lower().endswith(".pdf"):
        continue
    pdf_path = os.path.join(pdf_raw_dir, pdf)

    #in the map with a name (found earlier or filled by hand): move if not yet in pdf_clean
    row = rows.get(pdf)
    if row and row["method"] == "manual":
        if row["clean_name"] and os.path.exists(os.path.join(pdf_clean_dir, row["clean_name"])):
            print(f"Manual {pdf}: {row['clean_name']} is in pdf_clean; delete this pdf_raw copy by hand")
        else:
            print(f"Manual {pdf}: move it to pdf_clean as '{row['clean_name']}' by hand")
        continue
    if row and row["clean_name"]:
        clean_name = row["clean_name"]
        if not clean_name.endswith(".pdf") or "/" in clean_name:
            print(f"Check {pdf}: clean_name must be a file name ending in .pdf: {clean_name}")
        elif sum(r["clean_name"] == clean_name for r in rows.values()) > 1:
            print(f"Check {pdf}: clean_name {clean_name} is used by another PDF in the map")
        elif not os.path.exists(os.path.join(pdf_clean_dir, clean_name)):
            shutil.move(pdf_path, os.path.join(pdf_clean_dir, clean_name))
            print(f"Moved {pdf} -> {clean_name} ({row['method']})")
        elif same_file(pdf_path, os.path.join(pdf_clean_dir, clean_name)):
            os.remove(pdf_path)  # copy left by an earlier version of this script; pdf_clean has the same bytes
            print(f"Removed {pdf}: same file already in pdf_clean as {clean_name}")
        else:
            print(f"Check {pdf}: pdf_clean already has a different {clean_name}; nothing moved")
        continue

    print(f"Looking at PDF: {pdf}")
    with pymupdf.open(pdf_path) as doc:
        first_pages = " ".join(page_text(page) for page in list(doc)[:n_pages])
        title_guess = largest_font_text(doc[0]) if len(doc) else ""

    #1. DOI printed on the first pages -> Crossref record; check the record is this paper, not a cited one
    stem, method, note = None, "not_found", "no DOI on first pages"
    doi = find_doi(first_pages)
    if doi:
        print(f"    DOI: {doi}")
        try:
            metadata = works.doi(doi)
            note = "" if metadata else "DOI not in Crossref"
        except Exception as e:
            metadata, note = None, f"Crossref error: {e}"
        if metadata:
            stem, note = name_from(metadata, first_pages)
            method = "doi" if stem else "doi_unverified"

    #2. no verified DOI -> Crossref title search with the largest-font text, the page text, then the file name
    if stem is None:
        queries = [q for q in (title_guess, " ".join(first_pages.split()[:60]), os.path.splitext(pdf)[0].replace("_", " "))
                   if len(squash(q)) >= 15]
        found, found_doi, search_note = search_title(queries, first_pages)
        if found:
            stem, method, doi, note = found, "title", found_doi, ""
            print(f"    title search: {found_doi}")
        else:
            note = "; ".join(filter(None, [note, search_note]))

    #no verified record: clean_name left empty for manual entry; the PDF stays in pdf_raw
    if stem is None:
        print(f"    {method}: {note}; name it by hand (method = manual in {rename_map})")
        rows[pdf] = {"raw_name": pdf, "clean_name": "", "doi": doi or "", "method": method, "note": note}
        write_map()
        continue

    new_pdf_name = unique_name(stem, taken | set(os.listdir(pdf_clean_dir)))
    if new_pdf_name != f"{stem}.pdf":
        note = "; ".join(filter(None, [note, f"name collision: {stem}.pdf taken"]))
    taken.add(new_pdf_name)

    #move: the raw name is kept in the rename map
    shutil.move(pdf_path, os.path.join(pdf_clean_dir, new_pdf_name))
    rows[pdf] = {"raw_name": pdf, "clean_name": new_pdf_name, "doi": doi or "", "method": method, "note": note}
    write_map()
    print(f"    -> {new_pdf_name}")

todo = sorted(r["raw_name"] for r in rows.values() if not r["clean_name"])
check = sorted(r["raw_name"] for r in rows.values() if r["method"] != "manual"
               and r["clean_name"] and not os.path.exists(os.path.join(pdf_clean_dir, r["clean_name"])))
to_move = sorted(r["raw_name"] for r in rows.values() if r["method"] == "manual"
                 and not (r["clean_name"] and os.path.exists(os.path.join(pdf_clean_dir, r["clean_name"]))))
renamed = len(rows) - len(todo) - len(check) - len(to_move)
print(f"All done! Map: {rename_map} | renamed {renamed} | to name by hand {len(todo)} | manual, to move by hand {len(to_move)} | clean_name to check {len(check)}")
for pdf in todo:
    print(f"    to name: {pdf}")
for pdf in to_move:
    print(f"    to move: {pdf}")
for pdf in check:
    print(f"    to check: {pdf}")
