Utilities (vex_ast.utils)

This directory contains utility modules that provide supporting functionality for the VEX AST parser and other components.

Purpose

These modules encapsulate common tasks and data structures needed across the vex_ast package, promoting code reuse and separation of concerns.

Modules

Error Handling (errors.py):

ErrorType: An enum defining categories of errors (e.g., PARSER_ERROR, SEMANTIC_ERROR).

Error: A class representing a single error instance, containing the type, message, optional source location, and optional suggestion.

ErrorHandler: A central class for collecting and managing errors encountered during parsing or AST processing. It allows registering observers and can optionally raise exceptions immediately upon error detection.

VexAstError, VexSyntaxError: Custom exception classes for AST-related errors, with VexSyntaxError specifically for parsing issues.

Importance: Provides a robust way to handle and report problems found in the source code or during AST processing, crucial for user feedback and debugging.

Source Location (source_location.py):

SourceLocation: A dataclass representing a position or span within the original source code file. It includes line and column numbers (and optionally end line/column and filename).

Importance: Allows AST nodes and errors to be linked back to their origin in the source code, which is essential for accurate error reporting, debugging tools, and source mapping.

Usage

These utilities are primarily used internally by other parts of the vex_ast package:

The PythonParser uses the ErrorHandler to report syntax errors or issues during AST conversion. It uses SourceLocation to tag generated AST nodes with their origin.

AST Node classes store SourceLocation objects.

Visitors might use the ErrorHandler if they perform analysis that detects semantic errors.

Error messages often include the string representation of a SourceLocation.
