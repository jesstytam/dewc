import os
from pathlib import Path
from tqdm import tqdm
import shutil
import subprocess

import pymupdf
import pymupdf4llm

# from session_info2 import session_info

pdf_in_path = "data/papers_test/pdf_new"
pdf_done_path = "data/papers_test/pdf_done"
md_path = "data/papers_test/md"                # scanned PDFs: raw markdown for Step 0
md_agents_path = "data/papers_test/md_agents"  # text-layer PDFs: raw markdown straight to Step 1
md_opt_skipped = "\n<!-- md_opt: none; text-layer PDF, raw marker output, Step 0 skipped -->\n"


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


for fi in tqdm(os.listdir(pdf_in_path)):

    print(f"Processing {fi}...")

    pdf_src = os.path.join(pdf_in_path, fi)
    pdf_dst = os.path.join(pdf_done_path, fi)
    stem = Path(fi).stem
    md_marker_path = f"{md_path}/{stem}"
    md_name = f"{stem.replace(' ', '_')}.md"
    print(f"     MD marker path: {md_marker_path}")

    #scanned? (full-page images; an OCR text layer does not make it clean)
    with pymupdf.open(pdf_src) as doc:
        scanned = is_scanned(doc)

    if not scanned:
        md_dst_path = f"{md_agents_path}/{md_name}"
        if os.path.exists(md_dst_path):
            print(f"     {md_dst_path} exists; not overwritten.")
            continue
        print("     PDF has a text layer: raw markdown to md_agents, Step 0 skipped.")
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
            "--output_dir", md_path
        ])
        #move md file into md_agents and mark it as finished for Step 1
        md_old_path = f"{md_marker_path}/{stem}.md"
        print(f"     Moving {md_old_path} to {md_dst_path}.")
        shutil.move(md_old_path, md_dst_path)
        with open(md_dst_path, "a", encoding="utf-8") as f:
            f.write(md_opt_skipped)

    #scanned: raw text layer (if any) for Step 0, which reads the page images
    else:
        print("     PDF is scanned: raw markdown to md for Step 0.")
        md = pymupdf4llm.to_markdown(pdf_src)
        out = Path(f"{md_path}/{md_name}")
        out.write_text(md, encoding="utf-8")

    #move pdf
    shutil.move(pdf_src, pdf_dst)

    #remove new folders
    print("     Removing sub-folder.")
    if os.path.isdir(md_marker_path):
        shutil.rmtree(md_marker_path)

print("All done!")

# print(session_info(dependencies=True))
