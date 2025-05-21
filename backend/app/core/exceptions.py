from fastapi import HTTPException


class CustomException(HTTPException):
    """
    Custom exception class that extends FastAPI's HTTPException.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code=status_code, detail=message)


class DocumentProcessingException(CustomException):
    """Exception raised during document processing."""
    def __init__(self, message: str):
        super().__init__(status_code=500, message=f"Document processing error: {message}")


class DocumentNotFoundException(CustomException):
    """Exception raised when a document is not found."""
    def __init__(self, document_id: str):
        super().__init__(status_code=404, message=f"Document with ID {document_id} not found")


class UnauthorizedException(CustomException):
    """Exception raised for unauthorized access."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(status_code=401, message=message)


class FileTooLargeException(CustomException):
    """Exception raised when uploaded file is too large."""
    def __init__(self, max_size_mb: int):
        super().__init__(
            status_code=413,
            message=f"File too large. Maximum allowed size is {max_size_mb}MB"
        )


class UnsupportedFileTypeException(CustomException):
    """Exception raised when file type is not supported."""
    def __init__(self, file_type: str, supported_types: list):
        super().__init__(
            status_code=415,
            message=f"Unsupported file type: {file_type}. Supported types: {', '.join(supported_types)}"
        )