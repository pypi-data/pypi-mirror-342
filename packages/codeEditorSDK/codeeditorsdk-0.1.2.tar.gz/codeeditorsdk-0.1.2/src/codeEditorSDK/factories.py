from .core.codeEditor import CodeFileEditor
from .exception import UnsupportedLanguageError

class MultiLangEditorFactory:
    SUPPORTED_LANGUAGES = {'python', 'java', 'cpp', 'javascript', 'c'}
    
    @classmethod
    def get_editor(cls, lang: str) -> CodeFileEditor:
        lang = lang.lower()
        if lang not in cls.SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(lang)
        return CodeFileEditor(lang)