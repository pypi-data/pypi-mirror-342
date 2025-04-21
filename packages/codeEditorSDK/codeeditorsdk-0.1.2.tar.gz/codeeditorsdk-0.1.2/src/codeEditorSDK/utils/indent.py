from typing import List
from tree_sitter import Parser, Node
from tree_sitter_languages import get_language

class IndentHelper:
    def __init__(self, language: str):
        self.language = language
        self.parser = Parser()
        self.parser.set_language(get_language(language))
    
    def detect_indent(self, line: str) -> str:
        """Detect indentation characters at the beginning of a line"""
        indent = []
        for char in line:
            if char in (' ', '\t'):
                indent.append(char)
            else:
                break
        return ''.join(indent)
    
    def get_indent_level(self, lines: List[str], insert_pos: int) -> str:
        """Get the indentation of a specific line"""
        if not lines:
            return ''
        if insert_pos < len(lines):
            return self.detect_indent(lines[insert_pos])
        return self.detect_indent(lines[-1])
    
    def apply_language_rules(self, lines: List[str], insert_pos: int, base_indent: str) -> str:
        """Apply language-specific indentation rules"""
        if self.language in ['python', 'java', 'cpp', 'c']:
            if insert_pos > 0:
                prev_line = lines[insert_pos - 1].rstrip()
                open_brace = prev_line.count('{') - prev_line.count('}')
                if open_brace > 0:
                    return base_indent + ' ' * 4
                if self.language in ['c', 'cpp'] and prev_line.startswith('#'):
                    return ''
                if self.language == 'python':
                    indent_level = base_indent
                    for i in range(insert_pos-1, -1, -1):
                        line = lines[i].rstrip()
                        if not line:
                            continue
                        if line.endswith(':'):
                            indent_level += '    '
                        else:
                            break
                    return indent_level
        return base_indent
    
    def normalize_code_indent(self, code: str, target_indent: str) -> str:
        """Normalize code indentation"""
        lines = code.split('\n')
        min_indent = None
        for line in lines:
            stripped_line = line.lstrip(' \t')
            if not stripped_line:
                continue
            indent = line[:len(line) - len(stripped_line)]
            if min_indent is None or len(indent) < len(min_indent):
                min_indent = indent
        min_indent = min_indent or ''
        adjusted = []
        for line in lines:
            if line.startswith(min_indent):
                adjusted_line = target_indent + line[len(min_indent):]
            else:
                adjusted_line = target_indent + line.lstrip()
            adjusted.append(adjusted_line)
        return '\n'.join(adjusted)
    
    def _is_block_node(self, node: Node) -> bool:
        """Check whether this node represents a code block"""
        return node.type in {'suite', 'block'}
    
    def reindent_function_body(self, full_code: str, body_start: int, body_end: int, parent_indent: str = '') -> str:
        """Core reindentation logic for function bodies"""
        print("[DEBUG] Entering reindent_function_body")
        body_code = full_code[body_start:body_end]
        lines = body_code.splitlines()
        tree = self.parser.parse(bytes(body_code, "utf8"))
        root = tree.root_node
        indent_map = [0] * len(lines)

        def traverse(node: Node, level: int):
            start_line = node.start_point[0]
            end_line = node.end_point[0]
            
            # Update indent level for lines covered by this node
            for i in range(start_line, end_line + 1):
                if 0 <= i < len(indent_map):
                    indent_map[i] = max(indent_map[i], level)
            
            for child in node.children:
                # Handle function definitions
                if child.type == 'function_definition':
                    def_line = child.start_point[0]
                    if 0 <= def_line < len(indent_map):
                        indent_map[def_line] = level
                    
                    body_node = child.child_by_field_name("body")
                    if body_node:
                        traverse(body_node, level + 1)
                    
                    for grandchild in child.children:
                        if grandchild != body_node:
                            traverse(grandchild, level)
                
                # Handle control structures
                elif child.type in ['for_statement', 'while_statement', 'if_statement', 'try_statement']:
                    traverse(child, level)
                    body = child.child_by_field_name('consequence') if child.type == 'if_statement' else child.child_by_field_name('body')
                    if body and body.type in ['suite', 'block']:
                        traverse(body, level + 1)
                    if child.type == 'if_statement':
                        alternative = child.child_by_field_name('alternative')
                        if alternative and alternative.type == 'else_clause':
                            traverse(alternative, level)
                            else_body = alternative.child_by_field_name('body')
                            if else_body:
                                traverse(else_body, level + 1)
                
                # Handle block nodes
                elif self._is_block_node(child):
                    traverse(child, level + 1)
                
                # Other nodes stay at current level
                else:
                    traverse(child, level)

        traverse(root, 1)

        for i, (lvl, line) in enumerate(zip(indent_map, lines)):
            print(f"[DEBUG] Line {i+1:02d} | Indent Level = {lvl} | Line = {repr(line)}")

        base_indent = parent_indent
        unit = '    '
        final_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                final_lines.append('')
            else:
                final_lines.append(base_indent + (unit * indent_map[i]) + stripped)

        result = '\n'.join(final_lines)
        print("[DEBUG] Final re-indented body:\n", result)
        return result
    
    def reindent_node_region(self, full_code: str, node: Node, indent: str = '') -> str:
        """Reindent the region of the given node"""
        body_code = full_code[node.start_byte:node.end_byte]
        return self.normalize_code_indent(body_code, indent)
    
    def reindent_code_preserving_indent(self, code: str, reference_code: str) -> str:
        """Re-indent code while preserving indentation style from reference"""
        lines = reference_code.splitlines()
        base_indent = ""
        for line in lines:
            if line.strip():
                base_indent = self.detect_indent(line)
                break
        return self.normalize_code_indent(code, base_indent)