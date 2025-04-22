Code Parser (vex_ast.parser)

This directory contains the components responsible for parsing VEX V5 Python source code and constructing the Abstract Syntax Tree (AST).

Purpose

The parser's role is to take raw source code (as a string or from a file) and transform it into the structured AST representation defined in vex_ast.ast. It handles syntax rules, identifies different code constructs, and builds the corresponding tree of nodes.

Key Components

Interfaces (interfaces.py):

IParser: Protocol defining the essential parse() method that all parser implementations must provide.

BaseParser: An abstract base class providing common functionality, such as integrating with the ErrorHandler.

Node Factory (factory.py):

NodeFactory: Implements the Factory pattern. It provides methods (create_identifier, create_binary_operation, etc.) to instantiate specific AST node types defined in vex_ast.ast. This decouples the main parsing logic from the details of node creation and allows for easier management of node instantiation, including attaching source locations and potentially handling errors during creation.

Python Parser (python_parser.py):

PythonParser: The concrete implementation of IParser. It leverages Python's built-in ast module to parse the input Python code into a standard Python AST.

It then traverses the Python AST, using the NodeFactory to convert the standard Python nodes (ast.Assign, ast.Call, ast.BinOp, etc.) into the corresponding custom VEX AST nodes (Assignment, FunctionCall, BinaryOperation, etc.).

Provides convenience functions parse_string and parse_file.

Workflow

The user calls parse_string or parse_file.

An instance of PythonParser is created with the source code and an optional ErrorHandler.

The PythonParser uses Python's ast.parse to generate a standard Python AST.

The PythonParser walks through the Python AST. For each Python ast node, it determines the corresponding VEX AST node type.

It calls the appropriate create_... method on its internal NodeFactory instance, passing the necessary components (sub-expressions, statements, names, values) converted recursively.

The NodeFactory creates the VEX AST node, potentially adding source location information extracted from the original Python ast node.

This process continues recursively until the entire Python AST is converted into the custom VEX AST (Program node).

Any syntax errors during Python parsing or unsupported constructs during conversion are reported via the ErrorHandler.

The final Program node representing the VEX AST is returned.
