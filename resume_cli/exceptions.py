class ResumeCliError(Exception):
    """Base exception for resume-cli errors."""


class ResumeFileNotFoundError(ResumeCliError):
    """Raised when a required file does not exist."""


class InvalidPdfError(ResumeCliError):
    """Raised when a file is not a valid PDF."""


class PdfReadError(ResumeCliError):
    """Raised when a PDF cannot be read."""


class EmptyPdfTextError(ResumeCliError):
    """Raised when extracted PDF text is empty."""


class EmptyFileError(ResumeCliError):
    """Raised when a text file is empty."""


class ApiKeyMissingError(ResumeCliError):
    """Raised when API key is not configured."""


class AiCallError(ResumeCliError):
    """Raised when an AI API call fails."""


class JsonParseError(ResumeCliError):
    """Raised when AI response cannot be parsed as JSON."""


class ValidationError(ResumeCliError):
    """Raised when AI response fails schema validation."""
