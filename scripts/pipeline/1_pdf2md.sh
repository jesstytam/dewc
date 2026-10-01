#!/bin/bash

for file in data/papers/pdf_new/*

do

  echo "Extracting data from $file..."

  marker_single "$file" \
    --mode fast \
    --disable_ocr \
    --disable_image_extraction \
    --output_format markdown \
    --use_pdftext_reading_order true \
    --html_tables_in_markdown \
    --paginate_output \
    --page_separator "<!-- PAGE BREAK -->" \
    --output_dir data/papers/md/

  mv "$file" "data/papers/pdf_done/"

done

echo "All done!"