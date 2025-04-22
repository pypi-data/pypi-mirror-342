# VEX AST (`vex_ast`) - Public API Reference

This document describes the main functions and classes exposed by the `vex_ast` package, intended for users who want to parse VEX V5 Python code and interact with the resulting Abstract Syntax Tree (AST).

## Overview

The core workflow typically involves:

1.  Parsing source code (from a string or file) using `parse_string` or `parse_file`. This requires an optional `ErrorHandler` instance.
2.  Receiving a `Program` object, which is the root of the generated AST.
3.  Instantiating one or more `AstVisitor` subclasses (like `PrintVisitor`, `NodeCounter`, `VariableCollector`, or custom ones).
4.  Calling the visitor's `visit()` method with the `Program` node to traverse the AST and perform actions.
5.  Checking the `ErrorHandler` instance for any reported errors during parsing or visiting.

---

## Parsing Functions

These functions are the entry points for converting source code into an AST.

### `parse_string`

Parses VEX V5 Python code provided as a string.

**Signature:**

```python
def parse_string(
    source: str,
    filename: str = "<string>",
    error_handler: Optional[ErrorHandler] = None
) -> Program:


Arguments:

source (str): The string containing the Python code to parse.

filename (str, optional): The name to associate with the source code, used in error messages and source locations. Defaults to "<string>".

error_handler (Optional[ErrorHandler], optional): An instance of ErrorHandler to collect parsing errors. If None, a default ErrorHandler is created internally (which will raise VexSyntaxError on the first syntax error). It's recommended to provide your own handler to manage errors more flexibly.

Returns:

Program: The root node of the generated Abstract Syntax Tree.

Raises:

VexSyntaxError: If a syntax error is encountered during parsing and the error_handler is configured to raise errors immediately (or if no handler is provided).

VexAstError: For other internal parsing or AST conversion issues if the error_handler is configured to raise errors.

parse_file

Parses VEX V5 Python code read from a specified file.

Signature:

def parse_file(
    filepath: str,
    error_handler: Optional[ErrorHandler] = None
) -> Program:
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Arguments:

filepath (str): The path to the Python file to be parsed.

error_handler (Optional[ErrorHandler], optional): An instance of ErrorHandler to collect parsing errors. See parse_string for details.

Returns:

Program: The root node of the generated Abstract Syntax Tree.

Raises:

FileNotFoundError: If the specified filepath does not exist.

IOError: If there is an error reading the file.

VexSyntaxError: If a syntax error is encountered (see parse_string).

VexAstError: For other internal parsing errors (see parse_string).

Core AST Node
Program

Represents the root node of the entire Abstract Syntax Tree.

Description:

The Program node is the object returned by parse_string and parse_file. It serves as the entry point for traversing the AST using visitors.

Key Attribute:

body (List[IStatement]): A list containing the top-level statements (like function definitions, assignments, expression statements) found in the parsed code.

Usage:

You typically don't instantiate Program directly. You receive it from a parsing function and pass it to the visit() method of an AstVisitor.

ast_root: Program = parse_string("x = 1")
printer = PrintVisitor()
printer.visit(ast_root) # Pass the Program node to the visitor
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Standard Visitors

Visitors provide mechanisms to traverse and process the AST. You instantiate a visitor and then call its visit method on an AST node (usually the Program root).

PrintVisitor

Generates a formatted, indented string representation of the AST structure. Useful for debugging and inspection.

Instantiation:

printer = PrintVisitor()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Core Method:

visit(node: IAstNode) -> str: Traverses the AST starting from node (typically the Program root) and returns a multi-line string representing the tree.

Example:

ast_root = parse_string("y = a + 5")
visitor = PrintVisitor()
ast_string_representation = visitor.visit(ast_root)
print(ast_string_representation)
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
NodeCounter

Counts the number of nodes in the AST.

Instantiation:

counter = NodeCounter()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Core Method:

visit(node: IAstNode) -> int: Traverses the AST starting from node and returns the total count of nodes visited.

Additional Attribute:

counts_by_type (Dict[str, int]): After calling visit, this dictionary holds the counts for each specific node type encountered (e.g., {'Assignment': 1, 'BinaryOperation': 1, ...}).

Example:

ast_root = parse_string("def f():\n  return 10")
visitor = NodeCounter()
total_nodes = visitor.visit(ast_root)
print(f"Total nodes: {total_nodes}")
print(f"Nodes by type: {visitor.counts_by_type}")
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
VariableCollector

Collects the names of all variables referenced (read from) in the AST. Does not include variables only assigned to or function/class names being defined.

Instantiation:

collector = VariableCollector()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Core Method:

visit(node: IAstNode) -> Set[str]: Traverses the AST starting from node and returns a set containing the names of all referenced variables (identifiers used in a Load context).

Example:

code = """
x = 10
y = x + z
def my_func(p):
    q = p
"""
ast_root = parse_string(code)
visitor = VariableCollector()
referenced_vars = visitor.visit(ast_root)
print(f"Referenced variables: {referenced_vars}") # Output: {'x', 'z', 'p'}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Error Handling

Components for managing and reporting errors during parsing and processing.

ErrorHandler

Manages the collection and reporting of errors.

Instantiation:

# Option 1: Collect errors, don't raise exceptions immediately
handler = ErrorHandler(raise_on_error=False)

# Option 2: Raise VexSyntaxError/VexAstError on the first error
handler = ErrorHandler(raise_on_error=True) # Default behavior if omitted
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Key Methods:

get_errors() -> List[Error]: Returns a list of all Error objects collected so far.

has_errors() -> bool: Returns True if any errors have been collected, False otherwise. Useful after parsing with raise_on_error=False.

clear_errors() -> None: Removes all collected errors.

add_observer(observer: ErrorObserver) -> None: (Advanced) Registers a custom object to be notified whenever an error is added.

remove_observer(observer: ErrorObserver) -> None: (Advanced) Unregisters an observer.

Usage:

Typically, you create an ErrorHandler instance and pass it to parse_string or parse_file.

error_handler = ErrorHandler(raise_on_error=False)
try:
    ast = parse_string("x = 1 + ", error_handler=error_handler)
    if error_handler.has_errors():
        print("Parsing completed with non-fatal errors:")
        for err in error_handler.get_errors():
            print(f"- {err}")
    else:
        print("Parsing successful.")
        # Proceed with AST processing...
except VexAstError as e:
     # This shouldn't happen if raise_on_error=False, but good practice
     print(f"Unexpected VexAstError: {e}")
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
ErrorType

An Enum used within Error objects to categorize the type of error.

Values:

LEXER_ERROR

PARSER_ERROR

TYPE_ERROR

SEMANTIC_ERROR

INTERNAL_ERROR

Usage:

You typically check the error_type attribute of Error objects retrieved from ErrorHandler.get_errors().

VexSyntaxError

Exception raised specifically for syntax errors encountered during parsing when the ErrorHandler is configured to raise errors.

Inheritance: VexSyntaxError -> VexAstError -> Exception

Attribute:

location (Optional[SourceLocation]): May contain the location (line, column) where the syntax error occurred.

VexAstError

The base exception class for all errors originating from the vex_ast library. VexSyntaxError is a subclass.

This reference covers the main components needed to use the vex_ast library effectively for parsing and basic AST interaction. For more advanced use cases, you might need to delve into the specific AST node types in vex_ast.ast or create custom visitors inheriting from vex_ast.visitors.AstVisitor.

IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END