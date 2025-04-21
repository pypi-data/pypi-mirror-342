from typing import Optional
from tree_sitter import Parser
from tree_sitter_languages import get_language
import re


class ASTUnrollHelper:
    def __init__(self, language: str):
        self.language = language
        self.parser = Parser()
        self.parser.set_language(get_language(language))

        # Set supported loop and function types
        if language == "python":
            self.loop_types = {"for_statement", "while_statement"}
            self.func_type = "function_definition"
        elif language in ["java", "cpp", "c"]:
            self.loop_types = {"for_statement", "while_statement"}
            self.func_type = "function_definition" if language != "java" else "method_declaration"
        else:
            raise ValueError(f"Unsupported language: {language}")

    def unroll_first_loop(self, code: str, factor: int, func_name: str = None) -> str:
        """
        Unrolls the first detectable loop node (for or while) in the specified function. Supports Python, Java, C, and C++. Handles nested loops and function-scoped unrolling. Returns the full source code after unrolling.
        """
        tree = self.parser.parse(bytes(code, "utf8"))
        root = tree.root_node

        # Find the function body (or global scope)
        target_body = self.find_function_body(root, code, func_name) if func_name else root
        if not target_body:
            return code  

        # Find the first loop
        loop_node = self.find_first_loop(target_body)
        if not loop_node:
            return code  

        loop_body_node = loop_node.child_by_field_name("body")
        if not loop_body_node:
            return code

        loop_indent = self._detect_indent(code, loop_body_node.start_byte)
        body_lines = code[loop_body_node.start_byte:loop_body_node.end_byte].splitlines()
        indented_body = "\n".join(loop_indent + line.lstrip() for line in body_lines)
        unrolled_body = (indented_body + "\n") * factor

        # Return new code replacing the entire loop node
        return code[:loop_node.start_byte] + unrolled_body + code[loop_node.end_byte:]

    def find_function_body(self, node, code, func_name):
        if node.type == self.func_type:
            if func_name:
                id_node = next((c for c in node.children if c.type == "identifier"), None)
                if not id_node or code[id_node.start_byte:id_node.end_byte] != func_name:
                    return None
            return node.child_by_field_name("body")
        for child in node.children:
            result = self.find_function_body(child, code, func_name)
            if result:
                return result
        return None

    def find_first_loop(self, node):
        if node.type in self.loop_types:
            return node
        for child in node.children:
            result = self.find_first_loop(child)
            if result:
                return result
        return None

    def _detect_indent(self, source: str, pos: int) -> str:
        line_start = source.rfind('\n', 0, pos) + 1
        line_end = source.find('\n', line_start)
        line = source[line_start:line_end] if line_end != -1 else source[line_start:]
        match = re.match(r'^(\s*)', line)
        return match.group(1) if match else ''

    def find_function_node(self, root_node, text: str, func_name: str) -> Optional[object]:
        """
        Locate the specified function node in the AST. Supported languages: Python, Java, C, C++.
        """
        func_type = {
            'python': 'function_definition',
            'java': 'method_declaration',
            'c': 'function_definition',
            'cpp': 'function_definition'
        }.get(self.language, 'function_definition')

        def dfs(node):
            if node.type == func_type:
                id_node = next((c for c in node.children if c.type == 'identifier'), None)
                if id_node:
                    name = text[id_node.start_byte:id_node.end_byte]
                    if name == func_name:
                        return node
            for child in node.children:
                result = dfs(child)
                if result:
                    return result
            return None

        return dfs(root_node)
