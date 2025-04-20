# malama/pdfqa/reader.py

import os
import fitz  # PyMuPDF
from .exceptions import *
from .context import PDFContext

class PDFHandler:
    def __init__(self, file_path, start=None, end=None):
        self.file_path = file_path
        self.start = start
        self.end = end
        self.doc = None

        self._validate_and_load()

    def _validate_and_load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundErrorCustom(f"File not found: {self.file_path}")
        if not self.file_path.lower().endswith(".pdf"):
            raise FileTypeNotSupportedError("Only PDF files are supported.")

        self.doc = fitz.open(self.file_path)
        total_pages = len(self.doc)

        if self.start is not None and not isinstance(self.start, int):
            raise ValueError("Start page must be an integer.")
        if self.end is not None and not isinstance(self.end, int):
            raise ValueError("End page must be an integer.")

        if self.start is not None and (self.start < 1 or self.start > total_pages):
            raise ValueError(f"Start page {self.start} is out of bounds. PDF has {total_pages} pages.")
        if self.end is not None and (self.end < 1 or self.end > total_pages):
            raise ValueError(f"End page {self.end} is out of bounds. PDF has {total_pages} pages.")
        if self.end is not None and self.start is None:
            raise ValueError("End page is provided but start page is missing.")
        if self.end is not None and self.start is not None and self.start > self.end:
            raise ValueError(f"End page ({self.end}) cannot be less than start page ({self.start}).")

    def load(self):
        if self.doc is None:
            raise RuntimeError("PDF document is not loaded.")

        if self.start is not None and self.end is not None:
            start_idx = self.start - 1
            end_idx = self.end
        elif self.start is not None:
            start_idx = self.start - 1
            end_idx = self.start
        else:
            start_idx = 0
            end_idx = len(self.doc)

        text = "".join(self.doc[i].get_text() for i in range(start_idx, end_idx))

        if not text.strip():
            raise EmptyPDFError("The selected pages in the PDF file are empty.")

        PDFContext.set_text(text)
