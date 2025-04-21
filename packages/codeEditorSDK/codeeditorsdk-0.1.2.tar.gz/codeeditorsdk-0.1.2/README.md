# Code Editor SDK

A multi-language source code editing SDK using Tree-sitter. Supports Python, Java, C, C++, JavaScript.

## Features

- Smart code insertion (auto-locates method bodies)
- Syntax-safe deletion, update, query
- Auto-indentation based on language
- Supports Python, Java, C/C++, JavaScript
- Type-safe variable renaming with optional parameter renaming
- Type annotation conversion across functions and parameters
- Operator swapping inside target functions
- Loop unrolling via AST with customizable factors
- Conditional operator replacement in if-statements

## Install via GitHub
pip install git https://github.com/ZiYang-ucr/CodeEditor.git

## Example

```python
from code_editor import MultiLangEditorFactory

editor = MultiLangEditorFactory.get_editor("python")
editor.smart_insert("demo.py", 'print("inserted")')

from code_editor import MultiLangEditorFactory, EditBuilder

editor = MultiLangEditorFactory.get_editor("python")
builder = EditBuilder(editor, "demo.py")
builder.rename_var(old_name="radius", new_name="r", func="compute_area")\
       .change_type(from_type="float", to_type="double", func="compute_area")\
       .operator_swap(old="*", new="-", func="compute_area")\
       .insert_code('print("Debug info")')\
       .update_lines(10, 10, 'print("Updated line")')\
       .apply()
```