VEX AST Package (vex_ast)

This directory is the root of the vex_ast Python package. It orchestrates the different components of the VEX AST generation and processing system.

Purpose

The vex_ast package provides a unified interface for parsing VEX V5 Python code into an Abstract Syntax Tree (AST) and tools for working with that AST.

Structure

The package is organized into several sub-packages:

ast/: Contains the definitions for all AST node types, representing the structure of the parsed code. See vex_ast/ast/README.md.

parser/: Includes the parsing logic responsible for converting source code text into an AST instance. See vex_ast/parser/README.md.

visitors/: Provides implementations of the Visitor pattern for traversing, analyzing, or transforming the AST. See vex_ast/visitors/README.md.

utils/: Contains utility classes and functions, primarily for error handling and source location tracking. See vex_ast/utils/README.md.

Core Exports

The main components are exposed through the vex_ast/__init__.py file, making them easily accessible:

parse_string(source, ...): Parses Python code from a string.

parse_file(filepath, ...): Parses Python code from a file.

Program: The root node type of the generated AST.

PrintVisitor: A visitor to generate a string representation of the AST.

NodeCounter: A visitor to count nodes in the AST.

VariableCollector: A visitor to collect variable names used in the AST.

ErrorHandler: Class for managing errors during parsing and processing.

VexSyntaxError, VexAstError: Custom exception types.

Workflow

The typical workflow involves:

Using parse_string or parse_file from this package to generate an AST (Program object) from source code.

Instantiating one or more visitors from vex_ast.visitors (or custom ones).

Calling the visit method of the visitor with the root Program node to perform analysis, transformation, or other operations on the AST.

Using the ErrorHandler to manage and inspect any errors encountered during the process.
