import os
import re
import shutil
from tqdm import tqdm

import pymupdf
from crossref.restful import Works

#paths
pdf_raw_dir = "data/papers_test/pdf_raw"
pdf_clean_dir = "data/papers_test/pdf_clean"

#setup
doi_regex = r'\b10\.\d{4,9}/[-.;()/:\w]+'
works = Works()

#rename pdfs
for pdf in tqdm(os.listdir(pdf_raw_dir)):

    print(f"Looking at PDF: {pdf}")
    pdf_path = os.path.join(pdf_raw_dir, pdf)

    doc = pymupdf.open(pdf_path)
    for page in doc:
        text = page.get_text()

        #get doi
        doi = re.findall(doi_regex, text)
        if doi:
            print(f"    DOI: {doi}")
            # print(type(doi))
            break
        else:
            continue

    #get family name and year
    if doi:
        metadata = works.doi(doi[0])
        year = metadata["created"]["date-parts"][0][0]
        authors = metadata["author"]
        for auth in authors:
            family_name = auth["family"]
            if len(family_name)==1:
                new_pdf_name = f"{family_name}_{year}.pdf"
            elif len(family_name)>1:
                new_pdf_name = f"{family_name}_et_al_{year}.pdf"

    #rename pdf
    pdf_new_path = os.path.join(pdf_clean_dir, new_pdf_name)
    shutil.move(pdf_path, pdf_new_path)
    