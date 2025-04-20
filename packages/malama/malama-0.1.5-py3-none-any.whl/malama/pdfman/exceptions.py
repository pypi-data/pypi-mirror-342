# malama/pdfqa/exceptions.py

class FileNotFoundErrorCustom(Exception):
    def __init__(self, message="The specified file path was not found."):
        super().__init__(message)

class FileTypeNotSupportedError(Exception):
    def __init__(self, message="Only PDF files are supported."):
        super().__init__(message)

class EmptyPDFError(Exception):
    def __init__(self, message="The PDF file is empty."):
        super().__init__(message)

class NoPDFFound(Exception):
    def __init__(self, message="No PDF has been loaded yet."):
        super().__init__(message)

class EmptyQueryError(Exception):
    def __init__(self, message="The query is empty."):
        super().__init__(message)

class GeminiAPIEmptyError(Exception):
    def __init__(self, message="API key for Gemini must be provided."):
        super().__init__(message)
