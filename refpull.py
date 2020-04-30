#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: get it running for one PDF, then customize LAParams to work for another one
# 2. separate fixing pdf-converted text from MLA formatting

"docstring"

__author__ = "Alex Pickering"

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import argparse

class ref:
    """This class creates reference objects"""
    
    def __init__(self, position, author_1, author_2, author_3, author_4, author_5, title, date, placeofpub, publication, etal):
        self.position = position
        self.author_1 = author_1
        self.author_2 = author_2
        self.author_3 = author_3
        self.author_4 = author_4
        self.author_5 = author_5
        self.etal = etal
        self.title = title
        self.date = date
        self.placeofpub = placeofpub
        self.publication = publication


def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = StringIO()
    #layout = LAParams(all_texts=True)
    # For documentation on LAParams, see:
    # https://github.com/pdfminer/pdfminer.six/blob/develop/pdfminer/layout.py
    layout = LAParams(line_margin=0.3)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    device.close()
    retstr.close()
    return text


def ref_pull(text):
    start = r"\s*(references|bibliography)\s*"
    match = re.search(start, text, re.IGNORECASE)
    print("matched")
    if match:
        print("if stepped into")
        text = text[match.end():]
        # TODO create objects called refs
        # pull info using regex, place into elements of objects
        
        # regex patterns: (?=.*\()\b([A-Z][A-zÀ-ÿ]*\s[A-Z]+)[,|\s] 
        # authors: (?=.*\()\b([A-Z][A-zÀ-ÿ]*-*\s*[A-zÀ-ÿ]*\s[A-Z]+)[,|\s]
        # whole entries: ([A-Z]+.*\n)

    #text = re.sub(r'(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)', r"\1 \2", text)
    #text = re.sub(r'(.+)\n', r'\1', text)
    #text = re.sub(r'\n', r'\n\n', text)
    #text = re.sub(r'\n\n', r'\r', text)

    #return text.encode('utf-8')
    return text


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('--filepath', type=argparse.FileType('r'))
    parser.add_argument('--filepath', type=str)
    args = parser.parse_args()

    if not args.filepath:
        pdf = input("Enter PDF file name: ")
    else:
        pdf = args.filepath

    text = pdf_to_text(pdf)
    refs = ref_pull(text)
    if text == refs:
        print("Error: reference text unaltered")
    else:
        print(refs)
    
    #return (text)


if __name__ == '__main__':
    main()
