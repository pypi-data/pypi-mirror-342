class CodeEditorError(Exception):
    """Base exception for all code editor errors"""
    pass

class SyntaxValidationError(CodeEditorError):
    """Raised when syntax validation fails"""
    def __init__(self, message: str):
        super().__init__(f"Syntax validation failed: {message}")

class UnsupportedLanguageError(CodeEditorError):
    """Raised when requesting an unsupported language"""
    def __init__(self, language: str):
        super().__init__(f"Unsupported language: {language}")

class InsertionError(CodeEditorError):
    """Raised when code insertion fails"""
    pass