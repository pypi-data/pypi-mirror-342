# malama/pdfqa/llama_llm.py

import requests
from .base import LLMBase

class LlamaLLM(LLMBase):
    def __init__(self, api_key, model="llama3-70b-8192"):
        super().__init__(api_key)
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = model

    def _ask_with_model(self, context, question):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        prompt = f"""Context from PDF:\n{context[:12000]}\n\nUser Question: {question}"""

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You're a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
