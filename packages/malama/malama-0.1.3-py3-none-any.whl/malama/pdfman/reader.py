import os
import fitz  # PyMuPDF
import google.generativeai as genai
from .exceptions import *

class PDFGeminiAssistant:
    def __init__(self, api_key):
        if not api_key:
            raise GeminiAPIEmptyError("API key must be provided.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro-002")
        self.pdf_text = ""

    def load_pdf(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundErrorCustom(f"File not found at: {file_path}")

        if not file_path.lower().endswith('.pdf'):
            raise FileTypeNotSupportedError("Only PDF files are supported.")

        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.pdf_text = text
        if not self.pdf_text:
            raise EmptyPDFError()

    def ask_question(self, question):
        if not self.pdf_text:
            raise NoPDFFound()
        if not question.strip():
            raise EmptyQueryError()

        prompt = f"""Context from PDF:\n{self.pdf_text[:8000]} \n\nUser Question: {question}"""
        response = self.model.generate_content(prompt)
        return response.text.strip()
