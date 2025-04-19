class FileTypeNotSupportedError(Exception):
    """
    Raised when the provided file is not a PDF.
    """
    def __init__(self, message="Only PDF files are supported."):
        self.message = message
        super().__init__(self.message)


class FileNotFoundErrorCustom(Exception):
    """
    Raised when the provided file path does not exist.
    """
    def __init__(self, message="The specified file path was not found."):
        self.message = message
        super().__init__(self.message)


class EmptyPDFError(Exception):
    """
    Raised when the PDF file is empty or no text is extracted.
    """
    def __init__(self, message="The PDF appears to be empty or contains no readable text."):
        self.message = message
        super().__init__(self.message)

class GeminiAPIEmptyError(Exception):
    """
    Raised when there is on Gemini API.
    """
    def __init__(self, message="API key must be provided."):
        self.message = message
        super().__init__(self.message)

class EmptyQueryError(Exception):
    """
    Raised when the user provides an empty question/query.
    """
    def __init__(self, message="The query provided is empty. Please enter a valid question."):
        self.message = message
        super().__init__(self.message)

class NoPDFFound(Exception):
    """
    Raised when the user didn't provide any pdf and directly ask question.
    """
    def __init__(self, message="Please provide PDF, No PDF found."):
        self.message = message
        super().__init__(self.message)
