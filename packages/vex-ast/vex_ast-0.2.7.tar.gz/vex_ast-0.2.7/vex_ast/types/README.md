# VEX AST Types Package (vex_ast.types)

This package defines the type system used for the VEX V5 Robot Python language.

## Purpose

The type system provides a way to represent and reason about the types of values in VEX code. This information is used for type checking, code optimization, and other purposes.

## Structure

The package is organized into several modules:

*   `base.py`: Defines base classes for types.
*   `enums.py`: Defines enums for different type categories.
*   `objects.py`: Defines classes for representing objects.
*   `primitives.py`: Defines classes for representing primitive types (e.g., int, float, string, boolean).
*   `type_checker.py`: Implements the type checking logic.

## Key Concepts

*   **Types**: Represent the kind of value that a variable or expression can have.
*   **Type checking**: The process of verifying that the types in a program are consistent.

## Integration with Registry

The type system integrates seamlessly with the registry's category system:

- Object types (MOTOR, BRAIN, etc.) correspond to VexCategory entries
- Enum types map to valid parameter values
- Type validation works with function signatures

## Recent Updates

- Support for new VEX object types (Brain, Controller)
- Enhanced compatibility checking with category system
- Improved enum type validation
- Better integration with registry validation

## Usage

The type system is used internally by the VEX AST parser, type checker, and other tools. It is not typically accessed directly by users.

### Example Internal Usage

```python
from vex_ast.types import MOTOR, DIRECTION_TYPE, VELOCITY_UNITS
from vex_ast.types.type_checker import type_checker

# Validate parameter types
if type_checker.is_compatible(arg_type, MOTOR):
    # Process motor argument

# Check enum values
if value in DIRECTION_TYPE.values:
    # Valid direction value
```

## Type Hierarchy

```
VexType (base)
├── PrimitiveType
│   ├── NumericType
│   │   ├── IntegerType
│   │   └── FloatType
│   ├── BooleanType
│   └── StringType
├── ObjectType (MOTOR, BRAIN, etc.)
├── EnumType (DIRECTION_TYPE, etc.)
└── VoidType
```

## Future Extensions

- Support for custom object methods
- Advanced type inference
- Generic types for containers
- Union types for flexible parameters