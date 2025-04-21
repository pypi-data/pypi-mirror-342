from tree_sitter import Parser
from tree_sitter_languages import get_language

class SyntaxValidator:
    def __init__(self, language: str):
        self.language = language
        self.parser = Parser()
        self._init_parser()
        self.reserved_keywords = self._load_reserved_keywords()
        self.valid_operators = self._load_valid_operators()
        self.valid_types = self._load_valid_types()

    def _init_parser(self):
        """Initialize the parser"""
        try:
            self.parser.set_language(get_language(self.language))
        except Exception as e:
            raise RuntimeError(f"Parser initialization failed: {str(e)}")

    def _load_reserved_keywords(self) -> set:
        """Load reserved keywords"""
        keywords = {
            'python': {
                'False', 'None', 'True', 'and', 'as', 'assert', 'async',
                'await', 'break', 'class', 'continue', 'def', 'del', 'elif',
                'else', 'except', 'finally', 'for', 'from', 'global', 'if',
                'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
                'raise', 'return', 'try', 'while', 'with', 'yield'
            },
            'java': {
                'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
                'char', 'class', 'const', 'continue', 'default', 'do', 'double',
                'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
                'goto', 'if', 'implements', 'import', 'instanceof', 'int', 
                'interface', 'long', 'native', 'new', 'package', 'private',
                'protected', 'public', 'return', 'short', 'static', 'strictfp',
                'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
                'transient', 'try', 'void', 'volatile', 'while'
            },
            'cpp': {
                'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand',
                'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t',
                'char32_t', 'class', 'compl', 'const', 'constexpr', 'const_cast',
                'continue', 'decltype', 'default', 'delete', 'do', 'double',
                'dynamic_cast', 'else', 'enum', 'explicit', 'export', 'extern',
                'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int',
                'long', 'mutable', 'namespace', 'new', 'noexcept', 'not',
                'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private',
                'protected', 'public', 'register', 'reinterpret_cast', 'return',
                'short', 'signed', 'sizeof', 'static', 'static_assert',
                'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local',
                'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union',
                'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t',
                'while', 'xor', 'xor_eq'
            },
            'c': {
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
                'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
                'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
                'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef',
                'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas',
                '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic',
                '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
            }
        }
        return keywords.get(self.language, set())

    def _load_valid_operators(self) -> set:
        """Load valid operator set"""
        operators = {
            'python': {'+', '-', '*', '/', '>', '<', '==', '>=', '<=', '!=', '**', '//'},
            'java': {'+', '-', '*', '/', '>', '<', '==', '>=', '<=', '!=', '=', '++', '--'},
            'cpp': {'+', '-', '*', '/', '>', '<', '==', '>=', '<=', '!=', '=', '++', '--'},
            'c': {'+', '-', '*', '/', '>', '<', '==', '>=', '<=', '!=', '=', '++', '--', '&&', '||', '!', '~'}

        }
        return operators.get(self.language, set())

    def _load_valid_types(self) -> set:
        """Load supported basic type set"""
        valid_types = {
            'python': {
                'int', 'float', 'bool', 'str', 'bytes', 'list', 'dict', 'set', 'tuple', 'complex',
                'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64',
                'float16', 'float32', 'float64', 'double'
            },
            'java': {
                'byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char',
                'String', 'Integer', 'Long', 'Float', 'Double', 'Boolean', 'Character', 'BigInteger', 'BigDecimal'
            },
            'cpp': {
                'bool', 'char', 'wchar_t', 'char16_t', 'char32_t',
                'short', 'int', 'long', 'long long',
                'unsigned char', 'unsigned short', 'unsigned int', 'unsigned long', 'unsigned long long',
                'float', 'double', 'long double',
                'int8_t', 'int16_t', 'int32_t', 'int64_t',
                'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t',
                'size_t', 'ptrdiff_t'
            },
            'c': {
                'char', 'short', 'int', 'long', 'long long',
                'unsigned char', 'unsigned short', 'unsigned int', 'unsigned long', 'unsigned long long',
                'float', 'double', 'long double',
                'int8_t', 'int16_t', 'int32_t', 'int64_t',
                'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t',
                'size_t', 'bool'
            }
        }
        return valid_types.get(self.language, set())

    def validate_syntax(self, code: str) -> bool:
        """Validate the syntax correctness of full code"""
        tree = self.parser.parse(bytes(code, "utf8"))
        return not tree.root_node.has_error

    def validate_operator_replacement(self, old_op: str, new_op: str):
        """Validate basic legality of operator replacement"""
        # if len(old_op) != len(new_op):
        #     raise ValueError(f"Operator length mismatch: {old_op} -> {new_op}")
        if new_op not in self.valid_operators:
            raise ValueError(f"Invalid operator for {self.language}: {new_op}")

    def validate_variable_name(self, var_name: str):
        """Validate basic legality of variable name"""
        if not var_name.isidentifier():
            raise ValueError(f"Invalid identifier: {var_name}")
        if var_name in self.reserved_keywords:
            raise ValueError(f"Reserved keyword: {var_name}")

    def validate_operator_in_context(self, node, new_op: str) -> bool:
        """Validate operator replacement in syntax context"""
        try:
            parent = node.parent
            original = parent.text.decode('utf8')
            start = node.start_byte - parent.start_byte
            end = node.end_byte - parent.start_byte
            modified = original[:start] + new_op + original[end:]
            return self._validate_fragment(modified)
        except Exception:
            return False

    def validate_variable_in_context(self, node, new_var: str) -> bool:
        """Validate variable replacement in syntax context"""
        try:
            parent = node.parent
            original = parent.text.decode('utf8')
            start = node.start_byte - parent.start_byte
            end = node.end_byte - parent.start_byte
            modified = original[:start] + new_var + original[end:]
            return self._validate_fragment(modified)
        except Exception:
            return False

    def _validate_fragment(self, code_fragment: str) -> bool:
        """Validate syntax correctness of isolated code fragment"""
        temp_parser = Parser()
        temp_parser.set_language(get_language(self.language))
        tree = temp_parser.parse(bytes(code_fragment, 'utf8'))
        return not tree.root_node.has_error
    
    def validate_type_name(self, type_name: str):
        """Validate legality of type name"""
        if not type_name.isidentifier():
            raise ValueError(f"Invalid type name: {type_name}")
        if type_name in self.reserved_keywords:
            raise ValueError(f"Cannot use reserved keyword as type name: {type_name}")
        if type_name not in self.valid_types:
            raise ValueError(f"Unknown or unsupported type name: {type_name}")