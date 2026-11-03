import os
from pathlib import Path
from tqdm import tqdm
import shutil
import subprocess

import pymupdf
import pymupdf4llm

# from session_info2 import session_info

pdf_in_path = "data/papers_test/pdf_clean"  # renamed PDFs from 1_clean_pdf.py; they stay here (pdf_path in results)
md_raw_path = "data/papers_test/md_raw"     # raw markdown of every PDF; Step 0 optimises (scanned) or moves (text-layer) it to md_llm
md_llm_path = "data/papers_test/md_llm"     # Step 0 output, input of Step 1
#last line of each md_raw file: tells Step 0 whether to optimise it
pdf_type_line = {True: "\n<!-- pdf2md: scanned -->\n", False: "\n<!-- pdf2md: text-layer -->\n"}


def is_scanned(doc, n_pages=5, min_cover=0.7):
    """True if most checked pages are a full-page image (scan, with or without an OCR text layer)."""
    pages = range(1, len(doc)) if len(doc) > 1 else range(len(doc))  # skip page 1, often a cover page
    hits = checked = 0
    for i in list(pages)[:n_pages]:
        page = doc[i]
        area = page.rect.width * page.rect.height
        cover = max((r.width * r.height for img in page.get_images(full=True)
                     for r in page.get_image_rects(img[0])), default=0)
        hits += cover > min_cover * area
        checked += 1
    return hits > checked / 2


def converted(fi):
    """True if markdown exists for this PDF in md_raw (waiting for Step 0) or md_llm (done)."""
    return any(os.path.exists(f"{folder}/{Path(fi).stem}.md") for folder in (md_raw_path, md_llm_path))


for fi in tqdm(sorted(os.listdir(pdf_in_path))):
    if not fi.lower().endswith(".pdf"):
        continue
    if converted(fi):
        print(f"Skipping {fi}: markdown exists")
        continue

    print(f"Processing {fi}...")

    pdf_src = os.path.join(pdf_in_path, fi)
    stem = Path(fi).stem
    md_marker_path = f"{md_raw_path}/{stem}"
    md_dst_path = f"{md_raw_path}/{stem}.md"

    #scanned? (full-page images; an OCR text layer does not make it clean)
    with pymupdf.open(pdf_src) as doc:
        scanned = is_scanned(doc)

    if not scanned:
        print("     PDF has a text layer: marker markdown to md_raw; Step 0 moves it to md_llm unchanged.")
        subprocess.run([
            "marker_single", pdf_src,
            "--mode", "fast",
            "--disable_ocr",
            "--disable_image_extraction",
            "--output_format", "markdown",
            "--use_pdftext_reading_order", "true",
            "--html_tables_in_markdown",
            "--paginate_output",
            "--page_separator", "<!-- PAGE BREAK -->",
            "--output_dir", md_raw_path
        ])
        #marker writes md_raw/<stem>/<stem>.md; move it up to md_raw/<stem>.md
        shutil.move(f"{md_marker_path}/{stem}.md", md_dst_path)

    #scanned: raw text layer (if any) for Step 0, which reads the page images
    else:
        print("     PDF is scanned: raw markdown to md_raw; Step 0 optimises it into md_llm.")
        Path(md_dst_path).write_text(pymupdf4llm.to_markdown(pdf_src), encoding="utf-8")

    with open(md_dst_path, "a", encoding="utf-8") as f:
        f.write(pdf_type_line[scanned])

    #remove new folders
    print("     Removing sub-folder.")
    if os.path.isdir(md_marker_path):
        shutil.rmtree(md_marker_path)

print("All done!")

# print(session_info(dependencies=True))
