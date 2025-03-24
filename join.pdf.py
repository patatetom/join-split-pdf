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

def main():
    if len(sys.argv) < 3:
        print("Usage: pdf.join.py a.pdf b.pdf c.pdf ...")
        sys.exit(1)

    joined = writer()
    filename = None

    for pdf in sys.argv[1:]:
        try:
            print(f"Adding {pdf}...")
            with open(pdf, "rb") as handle:
                joined.append_pages_from_reader(reader(handle))
            filename = filename or os.path.splitext(pdf)[0] + "-joined.pdf"
        except FileNotFoundError:
            print(f"Error: the file {pdf} does not exist!")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing {pdf}: {e}")
            sys.exit(1)

    if os.path.exists(filename):
        print(f"Error: the file {filename} already exists!")
        sys.exit(1)

    print(f"Saving to {filename}...")
    try:
        with open(filename, "wb") as handle:
            joined.write(handle)
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
