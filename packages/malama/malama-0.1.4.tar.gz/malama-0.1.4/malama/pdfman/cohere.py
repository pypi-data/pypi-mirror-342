# malama/pdfqa/cohere_llm.py

import requests
from .base import LLMBase

class CohereLLM(LLMBase):
    def __init__(self, api_key, model="command-r-plus"):
        super().__init__(api_key)
        self.api_url = "https://api.cohere.ai/v1/chat"
        self.model = model

    def _ask_with_model(self, context, question):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""Context from PDF:\n{context[:12000]}\n\nUser Question: {question}"""

        data = {
            "model": self.model,
            "message": prompt,
            "temperature": 0.7,
            "p": 1.0,
            "stream": False
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["text"].strip()
