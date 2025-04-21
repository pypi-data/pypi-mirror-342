from pathlib import Path
from tree_sitter import Parser
from tree_sitter_languages import get_language
from codeEditorSDK.utils.indent import IndentHelper
from codeEditorSDK.utils.validation import SyntaxValidator
from typing import Optional, List, Dict, Any
from codeEditorSDK.core.codeEditor import CodeFileEditor

import re
import os

class EditBuilder:
    """
    A builder class for constructing a chain of editing operations
    to be applied in batch to a CodeFileEditor instance.
    """
    def __init__(self, editor: CodeFileEditor, file_path: str):
        self.editor = editor
        self.file_path = file_path
        self.edits: List[Dict[str, Any]] = []

    def operator_swap(self,
                      old: str,
                      new: str,
                      func: Optional[str] = None) -> 'EditBuilder':
        """Swap operators within the function or globally."""
        self.edits.append({
            "op": "operator_swap",
            "args": {"old": old, "new": new},
            "scope": {"func": func}
        })
        return self

    def rename_var(self,
                   old_name: str,
                   new_name: str,
                   func: Optional[str] = None,
                   include_param: bool = True) -> 'EditBuilder':
        """Rename a variable, optionally scoped to a function and including function parameters."""
        self.edits.append({
            "op": "rename_var",
            "args": {"old_name": old_name, "new_name": new_name, "include_param": include_param},
            "scope": {"func": func}
        })
        return self

    def change_type(self,
                    from_type: str,
                    to_type: str,
                    func: Optional[str] = None,
                    include_param: bool = True) -> 'EditBuilder':
        """Change the type of variables or function return types."""
        self.edits.append({
            "op": "change_type",
            "args": {"from_type": from_type, "to_type": to_type, "include_param": include_param},
            "scope": {"func": func}
        })
        return self

    def unroll_loop(self,
                    factor: int = 4,
                    func: Optional[str] = None) -> 'EditBuilder':
        """Unroll the first loop found in the specified function or globally."""
        self.edits.append({
            "op": "unroll_loop",
            "args": {"factor": factor},
            "scope": {"func": func}
        })
        return self

    def condition_operator_swap(self,
                                 old_op: str,
                                 new_op: str,
                                 func: Optional[str] = None) -> 'EditBuilder':
        """Swap condition operators in if-statements."""
        self.edits.append({
            "op": "condition_operator_swap",
            "args": {"old_op": old_op, "new_op": new_op},
            "scope": {"func": func}
        })
        return self

    def insert_code(self, code: str) -> 'EditBuilder':
        """Insert code snippet into the first valid function body."""
        if not isinstance(code, str):
            raise ValueError("insert_code expects a string code snippet.")
        if len(code) > 300 and not code.strip().startswith("\n"):
            raise ValueError("insert_code received unexpectedly large content. Double check formatting.")
        self.edits.append({
            "op": "smart_insert",
            "args": {"code": code.strip()},
            "scope": {}
        })
        return self
    
    def insert_code_lines(self, line: int, code: str) -> 'EditBuilder':
        """
        Insert code before the specified line. Line numbering starts at 1.
        All lines at and after the target line are shifted downward.
        """
        if not isinstance(code, str):
            raise ValueError("insert_code_lines expects a string code snippet.")
        if not isinstance(line, int) or line <= 0:
            raise ValueError("insert_code_lines expects a positive line number.")
        self.edits.append({
            "op": "insert_lines",
            "args": {"start_line": line, "code": code},
            "scope": {}
        })
        return self

    def delete_lines(self,
                     start_line: int,
                     end_line: int) -> 'EditBuilder':
        """Delete a range of lines from the file."""
        self.edits.append({
            "op": "delete_lines",
            "args": {"start_line": start_line, "end_line": end_line},
            "scope": {}
        })
        return self

    def update_lines(self,
                     start_line: int,
                     end_line: int,
                     new_code: str) -> 'EditBuilder':
        """Update a range of lines with new code."""
        self.edits.append({
            "op": "update_lines",
            "args": {"start_line": start_line, "end_line": end_line, "new_code": new_code},
            "scope": {}
        })
        return self

    def apply(self) -> 'CodeFileEditor':
        """Apply all recorded edit operations to the CodeFileEditor."""
        return self.editor.apply_edits(self.file_path, self.edits)