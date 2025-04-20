# malama/pdfqa/gemini_llm.py

import google.generativeai as genai
from .base import LLMBase

class GeminiLLM(LLMBase):
    def __init__(self, api_key):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro-002")

    def _ask_with_model(self, context, question):
        prompt = f"""Context from PDF:\n{context[:8000]}\n\nUser Question: {question}"""
        response = self.model.generate_content(prompt)
        return response.text.strip()
