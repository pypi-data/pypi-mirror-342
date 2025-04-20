# malama/pdfqa/base_llm.py

from abc import ABC, abstractmethod
from .context import PDFContext
from .exceptions import NoPDFFound, EmptyQueryError

class LLMBase(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    def ask(self, question):
        if not PDFContext.is_loaded():
            raise NoPDFFound("No PDF loaded yet.")
        if not question.strip():
            raise EmptyQueryError("The question is empty.")

        return self._ask_with_model(PDFContext.get_text(), question)

    @abstractmethod
    def _ask_with_model(self, context, question):
        pass
