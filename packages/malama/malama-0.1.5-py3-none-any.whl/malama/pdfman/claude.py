# malama/pdfqa/claude_llm.py

import anthropic
from .base import LLMBase

class ClaudeLLM(LLMBase):
    def __init__(self, api_key, model="claude-3-7-sonnet-20250219"):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def _ask_with_model(self, context, question):
        prompt = f"""Context from PDF:\n{context[:12000]}\n\nUser Question: {question}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()
