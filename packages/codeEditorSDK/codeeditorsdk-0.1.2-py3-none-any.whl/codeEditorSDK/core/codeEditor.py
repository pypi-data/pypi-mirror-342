from pathlib import Path
from tree_sitter import Parser
from tree_sitter_languages import get_language
from codeEditorSDK.utils.indent import IndentHelper
from codeEditorSDK.utils.validation import SyntaxValidator
from typing import Optional, List, Dict, Any
from codeEditorSDK.utils.ASTUnrollHelper import ASTUnrollHelper
import re


import os

class CodeFileEditor:
    def __init__(self, language: str):
        """
        Initialize a file-level code editor.
        :param language: Programming language (supported: python, java, cpp, javascript, etc.)
        """
        self.language = language
        self.parser: Optional[Parser] = None
        self.indent_helper = IndentHelper(language)
        self.validator = SyntaxValidator(language)
        self.unroller = ASTUnrollHelper(language)
        self._init_parser()


        
    def _init_parser(self):
        """Initialize the syntax parser"""
        try:
            # create instance of Parser
            self.parser = Parser()
            # use get_language to get the language parser
            self.parser.set_language(get_language(self.language))
        except Exception as e:
            raise RuntimeError(f"Parser initialization failed: {str(e)}")   

    def _apply_language_rules(self, lines: list, insert_pos: int, base_indent: str) -> str:
        """
        Apply language-specific indentation rules.
        :return: Adjusted indentation
        """
        if self.language in ['python', 'java', 'cpp', 'c']:
            if insert_pos > 0:
                prev_line = lines[insert_pos-1].rstrip()
                
                # general rule: detect unclosed braces
                open_brace = prev_line.count('{') - prev_line.count('}')
                if open_brace > 0:
                    indent_size = 4 if self.language in ['java', 'cpp', 'c'] else 4
                    return base_indent + ' ' * indent_size

                # C/C++ special rule: do not indent after preprocessor directives
                if self.language in ['c', 'cpp'] and prev_line.startswith('#'):
                    return ''  # preprocessor directives do not require indentation

                # Pytonh special rule: increase indent after a colon
                if self.language == 'python' and prev_line.endswith(':'):
                    return base_indent + '    '
        return base_indent

    def smart_insert(self, file_path: str, code: str) -> str:
        """
        Smart insert: auto detects the insertion point in a method body.
        Return the new file path with "_inserted" suffix.
        """
        path = Path(file_path)
        source_code = path.read_text(encoding="utf-8")
        tree = self.parser.parse(bytes(source_code, "utf8"))
        root = tree.root_node
        lines = source_code.splitlines()

        def find_method_body_insert_line(node):
            if self.language == "python":
                target_type = "function_definition"
                body_type = "block"
            elif self.language in ["java", "cpp", "c"]:
                target_type = "method_declaration" if self.language == "java" else "function_definition"
                body_type = "block"
            else:
                return None

            if node.type == target_type:
                body = node.child_by_field_name("body")
                if body and body.type == body_type:
                    return body.start_point[0] + 1
            for child in node.children:
                result = find_method_body_insert_line(child)
                if result is not None:
                    return result
            return None

        insert_line = find_method_body_insert_line(root)
        if insert_line is None:
            raise RuntimeError("No legal insertion point foun" \
            "" \
            "d for smart_insert")

        # print(f"[DEBUG] smart_insert wrote to: {file_path}")
    
        return self.insert(file_path, insert_line + 1, code)


    def insert(self, file_path: str, start_line: int, code: str) -> str:
        """
        Insert code at a specified line in the file, automatically adjusting indentation.
        :param file_path: Path to the source code file
        :param start_line: Line number to insert before (1-based)
        :param code: Code snippet to insert
        :return: Path to the new file with "_inserted" suffix
        """
        path = Path(file_path)
        
        # Read all lines with line breaks preserved
        lines = path.read_text(encoding='utf-8').splitlines(True)
        
        # Clamp the insert position to a valid line range (convert to 0-based index)
        insert_pos = max(1, min(start_line, len(lines) + 1)) - 1
        
        # Look upward for the nearest non-empty line to infer base indentation
        ref_line_idx = insert_pos - 1
        while ref_line_idx >= 0 and lines[ref_line_idx].strip() == '':
            ref_line_idx -= 1
        
        # Determine the base indentation of the reference line
        base_indent = self.indent_helper.detect_indent(lines[ref_line_idx]) if ref_line_idx >= 0 else ''
        
        # If the reference line ends with a colon in Python, increase indentation
        final_indent = base_indent + '    ' if self.language == 'python' and lines[ref_line_idx].rstrip().endswith(':') else base_indent
        
        # Normalize the code to be inserted with proper indentation
        normalized_code = self.indent_helper.normalize_code_indent(code, final_indent)
        
        # Ensure the inserted code ends with a newline
        formatted_code = normalized_code.rstrip('\n') + '\n'
        
        # Insert the new code into the line list
        new_lines = lines[:insert_pos] + [formatted_code] + lines[insert_pos:]
        
        # Combine lines back into a single string
        new_content = ''.join(new_lines)
        
        # Validate syntax of the new code
        self._assert_syntax(new_content, "insert")
        
        # Write the modified content to a new file with "_inserted" suffix
        return self._write_new(file_path, new_content, "_inserted")
 
    def delete(self, file_path: str, start_line: int, end_line: int) -> str:
        """
        Delete code in a specified line range.
        :param file_path: Target file path
        :param start_line: Start line (inclusive)
        :param end_line: End line (inclusive)
        :return: New file path (original name + _deleted suffix)
        """
        path = Path(file_path)
        lines = path.read_text(encoding='utf-8').splitlines(True)
        start = max(1, min(start_line, len(lines))) - 1
        end = max(start + 1, min(end_line + 1, len(lines)))
        new_lines = lines[:start] + lines[end:]
        new_content = ''.join(new_lines)
        self._assert_syntax(new_content, "delete")
        return self._write_new(file_path, new_content, "_deleted")

    def update(self, file_path: str, start_line: int, end_line: int, new_code: str) -> str:
        """
        Replace code in a specified line range (with automatic indentation).
        :param file_path: Target file path
        :param start_line: Start line (inclusive)
        :param end_line: End line (inclusive)
        :param new_code: New code content (can be multiline string)
        :return: New file path
        """
        path = Path(file_path)
        lines = path.read_text(encoding='utf-8').splitlines(True)

        start = max(1, min(start_line, len(lines))) - 1
        end = max(start + 1, min(end_line + 1, len(lines)))

        ref_line_idx = start
        while ref_line_idx >= 0 and lines[ref_line_idx].strip() == '':
            ref_line_idx -= 1
        base_indent = self.indent_helper.detect_indent(lines[ref_line_idx]) if ref_line_idx >= 0 else ''
        increase_indent = base_indent + '    '

        # if the reference line is a Python function definition, increase indent
        if self.language == 'python' and lines[ref_line_idx].strip().endswith(':'):
            indent_to_use = increase_indent
        else:
            indent_to_use = base_indent

        # insert new code with proper indentation
        lines_to_insert = new_code.strip().split('\n')
        formatted_lines = [(indent_to_use if i > 0 else base_indent) + line.strip() + '\n'
                        for i, line in enumerate(lines_to_insert)]

        # replace the specified range with formatted lines
        new_lines = lines[:start] + formatted_lines + lines[end:]
        new_content = ''.join(new_lines)

        try:
            self._assert_syntax(new_content, "update")
        except SyntaxError as e:
            print("[DEBUG] Preview of update content:")
            print(new_content)
            raise

        return self._write_new(file_path, new_content, "_updated")
    def query(self, file_path: str, start_line: int, end_line: int) -> str:
        """
        Query code in a specified line range.
        :param file_path: Target file path
        :param start_line: Start line (inclusive)
        :param end_line: End line (inclusive)
        :return: Code snippet as a string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start = max(1, min(start_line, len(lines)))
        end = max(start, min(end_line, len(lines)))
        
        return ''.join(lines[start-1:end])
    

    

    def swap_operator(self, file_path: str, old: str, new: str, func: Optional[str]=None) -> str:
        self.validator.validate_operator_replacement(old, new)
        
        text = Path(file_path).read_text(encoding='utf-8')
        if not func:
            # replace all occurrences in the file
            pattern = re.escape(old)
            new_text = re.sub(pattern, new, text)
            suffix = "_opswap"
        else:
            # based on function name, find the function body
            tree = self.parser.parse(bytes(text, 'utf8'))
            root = tree.root_node

            def find_target_func(node):
                func_type = {
                    'python': 'function_definition',
                    'java': 'method_declaration',
                    'c': 'function_definition',
                    'cpp': 'function_definition'
                }.get(self.language, 'function_definition')

                if node.type == func_type:
                    id_node = next((c for c in node.children if c.type == 'identifier'), None)
                    if id_node:
                        name = text[id_node.start_byte:id_node.end_byte]
                        if name == func:
                            return node.child_by_field_name('body')
                for child in node.children:
                    result = find_target_func(child)
                    if result:
                        return result
                return None

            body = find_target_func(root)
            if not body:
                raise ValueError(f"Function '{func}' not found in {file_path}")

            # replace within the function body
            start = body.start_byte
            end = body.end_byte
            print(f"[DEBUG] func_body start={start}, end={end}")
            print(text[start:end])
            func_body_text = text[start:end]
            replaced = re.sub(re.escape(old), new, func_body_text)
            new_text = text[:start] + replaced + text[end:]
            suffix = f"_opswap_{func}"

        # check syntax
        self._assert_syntax(new_text, "swap_operator")

        return self._write_new(file_path, new_text, suffix=suffix)

  
    def rename_var(self, file_path: str, old_name: str, new_name: str,
            func: Optional[str] = None,
            include_param: bool = True) -> str:
        """
        Rename variable safely. Supports limiting to a specific function
        and whether to rename parameters.
        """
        self.validator.validate_variable_name(new_name)

        text = Path(file_path).read_text(encoding='utf-8')
        tree = self.parser.parse(bytes(text, 'utf8'))
        root = tree.root_node

        if not func:
            # Global whole-word replacement
            pattern = rf'\b{re.escape(old_name)}\b'
            new_text = re.sub(pattern, new_name, text)
        else:
            # Find the specified function
            func_node = self.unroller.find_function_node(root, text, func)
            if not func_node:
                raise ValueError(f"Function '{func}' not found in {file_path}")

            # Handle parameter replacement if include_param is True
            if include_param:
                parameters_node = func_node.child_by_field_name('parameters')
                if parameters_node:
                    params_start = parameters_node.start_byte
                    params_end = parameters_node.end_byte
                    params_text = text[params_start:params_end]
                    new_params_text = re.sub(rf'\b{re.escape(old_name)}\b', new_name, params_text)
                    # Update the text with replaced parameters
                    text = text[:params_start] + new_params_text + text[params_end:]
                    # Re-parse the updated text to get new function node positions
                    new_tree = self.parser.parse(bytes(text, 'utf8'))
                    new_root = new_tree.root_node
                    func_node = self.unroller.find_function_node(new_root, text, func)
                    if not func_node:
                        raise ValueError(f"Function '{func}' not found after parameter replacement in {file_path}")

            body = func_node.child_by_field_name('body')
            if not body:
                return text

            start = body.start_byte
            end = body.end_byte
            func_body = text[start:end]

            # Replace variable in function body
            pattern = rf'\b{re.escape(old_name)}\b'
            replaced_body = re.sub(pattern, new_name, func_body)

            # Build temporary full code with replaced body
            temp_code = text[:start] + replaced_body + text[end:]

            # Re-indent the replaced region
            def_line = text[func_node.start_byte:start]
            parent_indent = self.indent_helper.detect_indent(def_line.splitlines()[0])
            new_body = self.indent_helper.reindent_function_body(
                full_code=temp_code,
                body_start=start,
                body_end=start + len(replaced_body),
                parent_indent=parent_indent
            )

            # Assemble final text
            new_text = (
                text[:start].rstrip() + '\n'
                + new_body
                + text[end:]
            )

        # Validate final syntax
        self._assert_syntax(new_text, "rename_var")

        suffix = f"_rename_{func}" if func else "_rename"
        return self._write_new(file_path, new_text, suffix=suffix)
    def _is_param_node(self, node):
        """
        Check if the node is a parameter node.
        """
        parent = node.parent
        return parent and parent.type in {'parameter', 'parameter_declaration', 'parameters'}



    def change_type(self,
                    file_path: str,
                    from_type: str,
                    to_type: str,
                    func: Optional[str] = None,
                    include_param: bool = True) -> str:
        """
        Change type annotations or declarations for Python, Java, C, and C++.
        Python parameter annotations only change when include_param=True;
        annotated assignments (e.g. pi: float) always change.
        """
        # check if the language is supported
        self.validator.validate_type_name(from_type)
        self.validator.validate_type_name(to_type)

        text = Path(file_path).read_text(encoding='utf-8')
        new_text = text

        # === Python branch === #
        if self.language == 'python':
            if func:
                # just a specific function
                tree = self.parser.parse(bytes(text, 'utf8'))
                root = tree.root_node
                func_node = self.unroller.find_function_node(root, text, func)
                if not func_node:
                    raise ValueError(f"Function '{func}' not found in {file_path}")
                # read function signature and body
                body = func_node.child_by_field_name('body')
                sig_start = func_node.start_byte
                sig_end = body.start_byte
                sig_text = new_text[sig_start:sig_end]
                body_text = new_text[sig_end:body.end_byte]
                # check include_param
                if include_param:
                    sig_text = re.sub(
                        rf':\s*{re.escape(from_type)}\b',
                        f': {to_type}',
                        sig_text
                    )
                # return type
                sig_text = re.sub(
                    rf'->\s*{re.escape(from_type)}\b',
                    f'-> {to_type}',
                    sig_text
                )
                # especially for Python, we need to handle annotated assignments
                body_text = re.sub(
                    rf':\s*{re.escape(from_type)}\b',
                    f': {to_type}',
                    body_text
                )
                # reassemble the new text
                new_text = (
                    new_text[:sig_start]
                    + sig_text
                    + body_text
                    + new_text[body.end_byte:]
                )
                suffix = f"_ctype_{func}"
            else:
                # replace all occurrences globally
                if include_param:
                
                    new_text = re.sub(
                        rf':\s*{re.escape(from_type)}\b',
                        f': {to_type}',
                        new_text
                    )
                # return type
                new_text = re.sub(
                    rf'->\s*{re.escape(from_type)}\b',
                    f'-> {to_type}',
                    new_text
                )
                # especially for Python, we need to handle annotated assignments
                new_text = re.sub(
                    rf':\s*{re.escape(from_type)}\b',
                    f': {to_type}',
                    new_text
                )
                suffix = "_ctype_python"

            self._assert_syntax(new_text, "change_type")
            return self._write_new(file_path, new_text, suffix)

        # JAVA/C/C++ AST
        if self.language in ['java', 'c', 'cpp']:
            tree = self.parser.parse(bytes(text, 'utf8'))
            root = tree.root_node
            replacements: List[tuple] = []

            if func:
                func_node = self.unroller.find_function_node(root, text, func)
                if not func_node:
                    raise ValueError(f"Function '{func}' not found in {file_path}")
                
                if include_param:
                    params = func_node.child_by_field_name('parameters')
                    if params:
                        for param in params.children:
                            tnode = param.child_by_field_name('type')
                            if tnode and text[tnode.start_byte:tnode.end_byte] == from_type:
                                replacements.append((tnode.start_byte, tnode.end_byte))
               
                ret = func_node.child_by_field_name('return_type')
                if ret and text[ret.start_byte:ret.end_byte] == from_type:
                    replacements.append((ret.start_byte, ret.end_byte))
               
                query = self.language_obj.query("""
                    (assignment_expression left: (_) @var right: (_) @val
                                          type: (primitive_type) @type)
                """)
                for node, tag in query.captures(func_node):
                    if tag == 'type' and text[node.start_byte:node.end_byte] == from_type:
                        replacements.append((node.start_byte, node.end_byte))
                # replace all found occurrences
                for start, end in sorted(replacements, reverse=True):
                    new_text = new_text[:start] + to_type + new_text[end:]
                suffix = f"_ctype_{func}"
            else:
                # replace all occurrences globally
                pattern = rf'\b{re.escape(from_type)}\b'
                new_text = re.sub(pattern, to_type, new_text)
                suffix = "_ctype"

            self._assert_syntax(new_text, "change_type")
            return self._write_new(file_path, new_text, suffix)

        # Default case: unsupported language
        raise NotImplementedError(
            f"change_type is supported only for python, java, c, cpp (given: {self.language})"
        )
    def unroll_loop(self, file_path: str, factor: int = 4, func: Optional[str] = None) -> str:
        """
        Perform loop unrolling using ASTUnrollHelper across multiple languages.
        Supports unrolling multiple or nested loops, and limiting to a specific function.
        The loop structure is replaced with repeated loop body content.
        """
        if not isinstance(factor, int) or factor <= 0:
            raise ValueError("Unroll factor must be a positive integer")

        # Step 1: Read source code and parse it with Tree-sitter
        text = Path(file_path).read_text(encoding='utf-8')
        tree = self.parser.parse(bytes(text, 'utf8'))
        root = tree.root_node

        # Step 2: Locate the target function body or use the root node
        target_body = self.unroller.find_function_body(root, text, func) if func else root
        if not target_body:
            return text  

        # Step 3: Find the first loop node in the body
        loop_node = self.unroller.find_first_loop(target_body)
        if not loop_node:
            return text 

        loop_body_node = loop_node.child_by_field_name("body")
        if not loop_body_node:
            return text

        # Step 4: Get loop body text and normalize indentation
        loop_body_text = text[loop_body_node.start_byte:loop_body_node.end_byte]
        # Break text into lines and get the line index of the loop
        lines = text.splitlines()
        loop_line = loop_node.start_point[0]
        # Determine base indent from the loop line
        base_indent = self.indent_helper.get_indent_level(lines, loop_line)
        # Apply language-specific indentation rules
        body_indent = self.indent_helper.apply_language_rules(lines, loop_line, base_indent)
        # Normalize loop body indentation with calculated indent
        normalized_body = self.indent_helper.normalize_code_indent(loop_body_text.strip('\n'), body_indent)
        # Repeat the loop body 'factor' times
        repeated_body = (normalized_body.rstrip('\n') + '\n') * factor

        # Step 5: Replace the original loop (header + body) with repeated body
        new_text = text[:loop_node.start_byte] + repeated_body + text[loop_node.end_byte:]

        # Step 6: Validate the new content and write to a file
        self._assert_syntax(new_text, "unroll_loop")
        return self._write_new(file_path, new_text, "_unroll")
    
    def apply_edits(self, file_path: str, edits: List[Dict[str, Any]]) -> str:
        self._merge_output = True  #set merge_output to True for chaining edits
        current = file_path
        for e in edits:
            op = e["op"]
            args = e.get("args", {})
            scope = e.get("scope", {})
            print(f"[DEBUG] Executing {op} on: {current}")


            try:
                if op == "operator_swap":
                    current = self.swap_operator(current, **args, **scope)

                elif op == "rename_var":
                    current = self.rename_var(current, **args, **scope)

                elif op == "change_type":
                    current = self.change_type(current, **args, **scope)

                elif op == "unroll_loop":
                    current = self.unroll_loop(current, **args, **scope)

                elif op == "condition_operator_swap":
                    current = self.swap_condition_operator(current, **args, **scope)

                elif op == "smart_insert":
                    if "code" not in args:
                        raise ValueError("Missing 'code' in args for smart_insert")
                    current = self.smart_insert(current, args["code"])

                elif op == "delete_lines":
                    current = self.delete(current, **args)

                elif op == "update_lines":
                    current = self.update(current, **args)

                elif op == "insert_lines":
                    current = self.insert(current, **args)
                else:
                    raise ValueError(f"Unknown op: {op}")

            except Exception as ex:
                raise RuntimeError(f"Edit operation '{op}' failed: {ex}")
            
                   
        final_text = Path(current).read_text(encoding="utf-8")
        chained_path = self._write_new(file_path, final_text, "_chained")
        return str(chained_path)


    def _write_new(self, old_path: str, content: str, suffix: str) -> str:
        """
        write the modified content to a new file.
        - if merge_output is True，then write to a file with "_chained" suffix
        - otherwise, write to a file with the specified suffix.
        """
        p = Path(old_path)
        if getattr(self, "_merge_output", False):
            output_path = p.parent / f"{p.stem.split('_')[0]}_chained{p.suffix}"
        else:
            output_path = p.parent / f"{p.stem}{suffix}{p.suffix}"

        output_path.write_text(content, encoding='utf-8')
        return str(output_path)
    
    def _assert_syntax(self, src: str, op: str):
        if not self.validator.validate_syntax(src):
            raise SyntaxError(f"{op} introduced syntax errors")
        



    def _get_param_names(self, func_node, text: str) -> set:
        """get all parameter names from a function node"""
        param_names = set()
        params_node = func_node.child_by_field_name("parameters")
        if not params_node:
            return param_names

        for child in params_node.children:
            if child.type == "identifier":
                param_name = text[child.start_byte:child.end_byte]
                param_names.add(param_name)

            # python and java may have default or typed parameters
            elif child.type in {"default_parameter", "typed_parameter"}:
                for sub in child.children:
                    if sub.type == "identifier":
                        param_name = text[sub.start_byte:sub.end_byte]
                        param_names.add(param_name)

        return param_names
    



    def swap_condition_operator(self,
                            file_path: str,
                            old_op: str,
                            new_op: str,
                            func: Optional[str] = None) -> str:
        """
        Replace conditional operators in all `if` statements within a specific function or globally.
        For example, old_op='>' and new_op='<' will replace all occurrences of '>' in conditions with '<'.
        """
        # Validate the legality of the operator replacement
        self.validator.validate_operator_replacement(old_op, new_op)

        # Read original source text and build AST
        text = Path(file_path).read_text(encoding='utf-8')
        tree = self.parser.parse(bytes(text, 'utf8'))
        root = tree.root_node

        # Determine the scope for replacement: function body or global
        scope = (self.unroller.find_function_node(root, text, func)
                 if func else root)
        if func and not scope:
            raise ValueError(f"Function '{func}' not found in {file_path}")

        # Recursively collect all 'condition' nodes from 'if_statement'
        cond_nodes: List = []
        def _collect_if_conditions(node):
            if node.type == "if_statement":
                cond = node.child_by_field_name("condition")
                if cond:
                    cond_nodes.append(cond)
            for child in node.children:
                _collect_if_conditions(child)
        _collect_if_conditions(scope)

        # Generate replacement spans for each condition node
        replacements: List[tuple] = []
        for cond in cond_nodes:
            start, end = cond.start_byte, cond.end_byte
            original = text[start:end]
            replaced = re.sub(re.escape(old_op), new_op, original)
            replacements.append((start, end, replaced))

        # Apply replacements in reverse order to avoid shifting positions
        new_text = text
        for start, end, replaced in sorted(replacements, key=lambda x: x[0], reverse=True):
            new_text = new_text[:start] + replaced + new_text[end:]

        # Validate final syntax and write updated file
        self._assert_syntax(new_text, "swap_condition_operator")
        suffix = f"_condop_{func}" if func else "_condop"
        return self._write_new(file_path, new_text, suffix)