import os
import Path
from tqdm import tqdm
import shutil
import subprocess

import pymupdf
import pymupdf4llm

pdf_in_path = "data/papers_test/pdf_new"
pdf_done_path = "data/papers_test/pdf_done"

for fi in tqdm(os.listdir(pdf_in_path)):

    print(f"Processing {fi}...")

    #check if pdf has text
    pdf_src = os.path.join(pdf_in_path, fi)
    pdf_dst = os.path.join(pdf_done_path, fi)
    first_page = pymupdf.open(pdf_src)[0]

    #text?
    text = first_page.get_text()
    if text.strip():
        print("     PDF is clean.")
        subprocess.run([
            "marker_single", pdf_src, 
            "--mode fast", 
            "--disable_ocr", 
            "--disable_image_extraction", 
            "--output_format markdown", 
            "--use_pdftext_reading_order", "true", 
            "--html_tables_in_markdown", 
            "--paginate_output", 
            "--page_separator", "<!-- PAGE BREAK -->", 
            "--output_dir", f"data/papers/md/{fi}"
        ])

    #image?
    images = first_page.get_images()
    if images:
        print("     PDF was scanned, using ORC.")
        md = pymupdf4llm.to_markdown(pdf_src)
        out = Path(f"data/papers/md/{fi}.md")
        out.write_text(md, encoding="utf-8")

    #move
    pdf_move = os.path.join(pdf_done_path, fi)
    shutil.move(pdf_src, pdf_dst)

print("All done!")