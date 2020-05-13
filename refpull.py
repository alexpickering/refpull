#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: get working for second pdf


"docstring"

__author__ = "Alex Pickering"

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import os
from io import StringIO
import argparse
import re


class Reference(object):
    """This class creates reference objects"""
    
    def __init__(self, title, date, placeofpub, publication, raw):
        self.authors     = []
        self.title       = title
        self.date        = date
        self.placeofpub  = placeofpub
        self.publication = publication
        self.raw         = raw

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
        # TODO create objects called References
        # pull info using regex, place into elements of objects
        
        # regex patterns: (?=.*\()\b([A-Z][A-zÀ-ÿ]*\s[A-Z]+)[,|\s] 
        # authors: (?=.*\()\b([A-Z][A-zÀ-ÿ]*-*\s*[A-zÀ-ÿ]*\s[A-Z]+)[,|\s]
        # whole entries: ([A-Z]+.*\n)

    text = re.sub(r'(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)', r"\1 \2", text)
    text = re.sub(r'(.+)\n', r'\1', text)
    text = re.sub(r'\n', r'\n\n', text)
    text = re.sub(r'\n\n', r'\r', text)

    # return text.encode('utf-8')
    return text

def parse_to_list(refs):
    ref_list = refs.split('\x0c')[0]
    ref_list = ref_list.split('\r')
    ref_list = [ref.strip() for ref in ref_list if ref.strip()]
    return ref_list

def second_parse_to_list(refs):
    # TODO: add find duplicate entries (headers), and delete, adding special char after last one
    pass
    # return ref_list

    
def save_to_file(ref_list, name):
    if isinstance(ref_list, str):
        with open(name + '.txt', 'w+') as f:
            f.write(ref_list)
    else:
        with open(name + '.txt', 'w+') as f:
            for ix in range(len(ref_list)):
                f.write("{}. {}\n".format(ix+1, ref_list[ix]))
                #f.write(f"{ix+1}. {ref_list[ix]}\n")


def pdf_to_reflist(pdf):
    text = pdf_to_text(pdf)
    text_block = ref_pull(text)
    if text == text_block:
        raise Exception("Error: reference text unaltered")

    refs = parse_to_list(text_block)
    return refs


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
    text_block = ref_pull(text)
    if text == text_block:
        raise Exception("Error: reference text unaltered")
    refs = parse_to_list(text_block)


    save_to_file(text_block, 'text_block')
    save_to_file(refs, 'refs')
    # refs = second_parse_to_list(text_block)
    save_to_file(refs, 'refs2')
    #return (text)


if __name__ == '__main__':
    main()
