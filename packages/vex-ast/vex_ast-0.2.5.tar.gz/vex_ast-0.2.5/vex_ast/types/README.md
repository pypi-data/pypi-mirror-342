# VEX AST Types Package (vex_ast.types)

This package defines the type system used for the VEX V5 Robot Python language.

Purpose

The type system provides a way to represent and reason about the types of values in VEX code. This information is used for type checking, code optimization, and other purposes.

Structure

The package is organized into several modules:

*   `base.py`: Defines base classes for types.
*   `enums.py`: Defines enums for different type categories.
*   `objects.py`: Defines classes for representing objects.
*   `primitives.py`: Defines classes for representing primitive types (e.g., int, float, string, boolean).
*   `type_checker.py`: Implements the type checking logic.

Key Concepts

*   Types: Represent the kind of value that a variable or expression can have.
*   Type checking: The process of verifying that the types in a program are consistent.

Usage

The type system is used internally by the VEX AST parser, type checker, and other tools. It is not typically accessed directly by users.
