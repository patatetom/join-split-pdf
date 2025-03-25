#!/bin/env python
#
# Python script relying on PyPDF2 to split
# a PDF document passed as a parameter into pieces.
# The splitting can be on a single page or a group
# of pages (eg., 1, 2, 3-6, 8-).
# The requested order is preserved (eg. 8-6).
# 

import os
import re
import sys
from PyPDF2 import PdfReader as reader, PdfWriter as writer

if len(sys.argv) < 3:
    sys.exit("Usage: split.pdf.py x.pdf y y-z -y y-")

one_page = re.compile(r"^([1-9]\d*)-\1$")
split_pattern = re.compile(r"^([1-9]\d*|[1-9]\d*-|-[1-9]\d*|[1-9]\d*-[1-9]\d*)$")

args = sys.argv[2:]
filename = sys.argv[1]

for arg in args:
    if not split_pattern.search(arg):
        sys.exit(f"Error: invalid cut {arg}")
    change = one_page.findall(arg)
    if change:
        args[args.index(arg)] = change.pop()

args = set(args)

print(f"Reading {filename}...")
try:
    pdf = reader(open(filename, "rb"))
    max_page = len(pdf.pages)
except FileNotFoundError:
    sys.exit(f"Error: {filename} does not exist")
except Exception as e:
    sys.exit(f"Error: {e}")

for arg in args:
    print(f"Extracting {arg}...")
    split = writer()
    split.flag = False
    slices = set()

    if "-" not in arg:
        arg = int(arg)
        slices.add(arg - 1)
    else:
        start, stop = arg.split("-")
        if not start:
            stop = int(stop)
            slices.add(range(stop))
        elif not stop:
            start = int(start)
            slices.add(range(start - 1, max_page))
        else:
            start, stop = int(start), int(stop)
            if start > stop:
                slices.add(range(start - 1, stop - 2, -1))
            else:
                slices.add(range(start - 1, stop))

    for slice in slices:
        for page in slice:
            if page >= max_page:
                print(f"Warning: page {page + 1} does not exist")
            else:
                split.add_page(pdf.pages[page])
                split.flag = True

    if split.flag:
        rename = os.path.splitext(filename)[0] + f"-{arg}.pdf"
        print(f"Saving to {rename}...")
        if os.path.exists(rename):
            print(f"Error: {rename} already exists")
        else:
            try:
                with open(rename, "wb") as handle:
                    split.write(handle)
            except Exception as e:
                print(f"Error: {e}")
