# malama/pdfqa/mistral_llm.py

import requests
from .base import LLMBase

class MistralLLM(LLMBase):
    def __init__(self, api_key, model="mistral-medium"):
        super().__init__(api_key)
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def _ask_with_model(self, context, question):
        prompt = f"""Context from PDF:\n{context[:8000]}\n\nUser Question: {question}"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an assistant that answers questions based on PDF content."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.api_url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Mistral API Error {response.status_code}: {response.text}")

        return response.json()['choices'][0]['message']['content'].strip()
