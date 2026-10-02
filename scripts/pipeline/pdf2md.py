import os
from pathlib import Path
from tqdm import tqdm
import shutil
import subprocess

import pymupdf
import pymupdf4llm

pdf_in_path = "data/papers_test/pdf_new"
pdf_done_path = "data/papers_test/pdf_done"
md_path = "data/papers_test/md"

for fi in tqdm(os.listdir(pdf_in_path)):

    print(f"Processing {fi}...")

    #check if pdf has text
    pdf_src = os.path.join(pdf_in_path, fi)
    pdf_dst = os.path.join(pdf_done_path, fi)
    first_page = pymupdf.open(pdf_src)[0]

    #text?
    text = first_page.get_text()
    md_marker_path = f"{md_path}/{Path(fi).stem}"
    if text.strip():
        print("     PDF is clean.")
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
        #move md file into the parent md folder
        md_old_path = f"{md_marker_path}/{Path(fi).stem}.md"
        print(f"     Moving {md_old_path} into parent dir.")
        shutil.move(md_old_path, md_path)
        
    #image?
    else:
        print("     PDF text not detected, using ORC instead.")
        md = pymupdf4llm.to_markdown(pdf_src)
        out = Path(f"data/papers_test/md/{Path(fi).stem}.md")
        out.write_text(md, encoding="utf-8")

    #move pdf
    pdf_move = os.path.join(pdf_done_path, fi)
    shutil.move(pdf_src, pdf_dst)

    #remove new folders
    print("     Removing sub-folder.")
    if os.path.isdir(md_marker_path):
        shutil.rmtree(md_marker_path)

print("All done!")