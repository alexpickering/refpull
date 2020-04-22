# refpull.py

## Summary

Refpull takes PDFs of MLA-formatted academic papers as input, and outputs the "References" Section in a .txt file.


## Description

Refpull.py takes a PDF as input, and determines if it is primarily text-based or image-based. If image-based, a popular Python OCR called PDF2txt.py is used to pull the text. Refpull then uses regex expressions to extract the "References" section from the text. 
