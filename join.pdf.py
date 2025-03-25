#!/bin/env python
#
# Small python script relying on PyPDF2 to assemble
# together PDF documents passed as parameters.
# The produced document will bear the name of the first document
# to which the string "-joined.pdf" will have been added.
#

import os
import sys
from PyPDF2 import PdfReader as reader, PdfWriter as writer

if len(sys.argv) < 3:
    sys.exit("Usage: pdf.join.py x.pdf y.pdf z.pdf ...")

joined = writer()
filename = None

for pdf in sys.argv[1:]:
    try:
        print(f"Adding {pdf}...")
        with open(pdf, "rb") as handle:
            joined.append_pages_from_reader(reader(handle))
        filename = filename or os.path.splitext(pdf)[0] + "-joined.pdf"
    except FileNotFoundError:
        sys.exit(f"Error: {pdf} does not exist")
    except Exception as e:
        sys.exit(f"Error: {e}")

if os.path.exists(filename):
    sys.exit(f"Error: {filename} already exists")

print(f"Saving to {filename}...")
try:
    with open(filename, "wb") as handle:
        joined.write(handle)
except Exception as e:
    sys.exit(f"Error: {e}")
