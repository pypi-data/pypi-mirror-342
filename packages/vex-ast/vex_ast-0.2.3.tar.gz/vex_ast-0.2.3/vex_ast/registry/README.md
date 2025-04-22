# VEX AST Registry Package (vex_ast.registry)

This package manages the registration and organization of VEX V5 Robot Python language features, including functions, objects, and other elements.

Purpose

The registry provides a centralized system for defining and accessing information about VEX-specific language constructs. This information is used by the parser, type checker, and other tools to understand and process VEX code.

Structure

The package is organized into several modules:

*   `categories.py`: Defines categories for organizing registry entries.
*   `language_map.py`: Maps VEX language features to their Python equivalents.
*   `registry.py`: Implements the core registry logic.
*   `signature.py`: Defines the structure for function signatures.
*   `simulation_behavior.py`: Specifies how VEX features should behave in a simulation environment.
*   `validation.py`: Provides validation rules for registry entries.
*   `functions/`: Contains submodules for specific function categories (e.g., drivetrain, motor, sensors).

Key Concepts

*   Registration: VEX language features are registered with the registry, providing metadata about their syntax, semantics, and simulation behavior.
*   Organization: The registry organizes features into categories and subcategories for easy access and management.
*   Validation: Registry entries are validated to ensure consistency and correctness.

Usage

The registry is used internally by the VEX AST parser and other tools. It is not typically accessed directly by users.
