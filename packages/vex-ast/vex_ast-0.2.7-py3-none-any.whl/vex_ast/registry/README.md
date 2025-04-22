# VEX AST Registry Package (vex_ast.registry)

This package manages the registration and organization of VEX V5 Robot Python language features, including functions, objects, and their semantic behaviors.

## Purpose

The registry provides a centralized system for defining and accessing information about VEX-specific language constructs. It powers intelligent parsing, type checking, and simulation capabilities by maintaining a comprehensive database of VEX functions and their properties.

## Architecture

### Core Components

*   `categories.py`: Implements the dual-axis categorization system
    - `VexCategory`: Defines what a component is (MOTOR, SENSOR, DISPLAY, etc.)
    - `BehaviorType`: Defines what a component does (CONTROL, READ, CONFIG, etc.)
    - `SubCategory`: Provides granular classification within categories
    - `FunctionCategorizer`: Intelligent categorization based on name and description

*   `api.py`: Clean API layer for registry access
    - Abstracts internal implementation details
    - Provides intuitive query methods
    - Maintains backward compatibility

*   `registry.py`: Core registry implementation
    - Thread-safe singleton pattern
    - Efficient lookup structures
    - Category/behavior indexing

*   `signature.py`: Function signature system
    - Parameter definitions and validation
    - Return type tracking
    - Language mapping (Python/C++)

### Function Organization

Functions are registered using a multi-dimensional classification:

```
Component → Category (what it is) → Behavior (what it does) → Subcategory (specific role)
Example: motor.spin → MOTOR → CONTROL → MOTOR_SPIN
```

## Usage

### Basic Registry Access

```python
from vex_ast.registry.api import registry_api

# Get functions by category
motor_functions = registry_api.get_functions_by_category(VexCategory.MOTOR)

# Get functions by behavior
control_functions = registry_api.get_functions_by_behavior(BehaviorType.CONTROL)

# Combined queries
motor_control = registry_api.get_functions_by_category_and_behavior(
    VexCategory.MOTOR, 
    BehaviorType.CONTROL
)

# Validate function calls
valid, error = registry_api.validate_call("motor.spin", args, kwargs)
```

### Function Registration

```python
from vex_ast.registry.signature import VexFunctionSignature, VexFunctionParameter
from vex_ast.registry.categories import VexCategory, BehaviorType

# Define function signature
signature = VexFunctionSignature(
    name="spin",
    return_type=VOID,
    parameters=[
        VexFunctionParameter("direction", DIRECTION_TYPE),
        VexFunctionParameter("velocity", FLOAT, 50.0),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM")
    ],
    description="Spin the motor in the specified direction",
    category=VexCategory.MOTOR,
    behavior=BehaviorType.CONTROL,
    python_name="spin",
    cpp_name="spin",
    object_type=MOTOR,
    method_name="spin"
)

# Register the function
registry.register_function(signature)
```

## Backward Compatibility

The registry maintains full backward compatibility with legacy systems:
- `SimulationCategory` enum is preserved and mapped to new categories
- Old API methods continue to work
- Automatic conversion between old and new category systems

## Extension Points

Extend the registry by:
1. Adding new `VexCategory` values
2. Defining new `BehaviorType` entries
3. Creating custom `SubCategory` classifications
4. Implementing specialized validation logic