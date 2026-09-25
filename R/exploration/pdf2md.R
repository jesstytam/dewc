library("pdftools")

test_pdf <- pdf_text("data/papers/29339.pdf")
cat(test_pdf[1], sep = "", fill = FALSE, labels = NULL, append = FALSE)

write(test_pdf, "data/texts/29339.txt")
