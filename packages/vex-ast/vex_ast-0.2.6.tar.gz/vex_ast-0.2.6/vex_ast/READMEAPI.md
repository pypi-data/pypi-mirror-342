# VEX AST Registry API Reference

The Registry API provides a comprehensive interface for accessing and querying VEX function information in the AST system.

## Core API

### Registration and Access

#### `registry_api`
Singleton instance providing access to all registry functionality.

```python
from vex_ast.registry.api import registry_api
```

### Function Queries

#### `get_function(name: str, language: str = "python") -> Optional[VexFunctionSignature]`
Retrieve a function signature by name.

```python
spin_function = registry_api.get_function("spin")
```

#### `get_functions_by_category(category: VexCategory) -> List[VexFunctionSignature]`
Get all functions in a specific category.

```python
motor_functions = registry_api.get_functions_by_category(VexCategory.MOTOR)
```

#### `get_functions_by_behavior(behavior: BehaviorType) -> List[VexFunctionSignature]`
Get all functions with a specific behavior.

```python
control_functions = registry_api.get_functions_by_behavior(BehaviorType.CONTROL)
```

#### `get_functions_by_category_and_behavior(category: VexCategory, behavior: BehaviorType) -> List[VexFunctionSignature]`
Get functions matching both category and behavior.

```python
motor_control = registry_api.get_functions_by_category_and_behavior(
    VexCategory.MOTOR,
    BehaviorType.CONTROL
)
```

### Method Access

#### `get_method(object_type: Union[VexType, str], method_name: str) -> Optional[VexFunctionSignature]`
Get a method signature for an object type.

```python
spin_method = registry_api.get_method(MOTOR, "spin")
```

### Validation

#### `validate_call(function_name: str, args: List[Any], kwargs: Dict[str, Any], language: str = "python") -> Tuple[bool, Optional[str]]`
Validate a function call against its signature.

```python
valid, error = registry_api.validate_call("motor.spin", [FORWARD, 50, "RPM"], {})
```

### Category Enumerations

#### VexCategory
- `MOTOR`: Motor control functions
- `DRIVETRAIN`: Drivetrain control functions
- `SENSOR`: Sensor reading functions
- `DISPLAY`: Display output functions
- `TIMING`: Timing control functions
- `COMPETITION`: Competition control functions
- `CONTROLLER`: Controller input functions
- `BRAIN`: Brain functions
- `UTILITY`: Utility functions
- `EVENT`: Event handling

#### BehaviorType
- `CONTROL`: Actively controls/changes state
- `READ`: Reads/retrieves information
- `CONFIG`: Configuration/setup
- `OUTPUT`: Produces output (display, signals)
- `EVENT`: Event handling/callbacks

## Advanced Usage

### Creating Custom Queries

```python
# Find all motor functions that read data
motor_readers = [
    func for func in registry_api.get_functions_by_category(VexCategory.MOTOR)
    if func.behavior == BehaviorType.READ
]

# Find all functions with specific subcategories
spin_functions = registry_api.get_functions_by_subcategory(SubCategory.MOTOR_SPIN)
```

### Registry Extension

```python
from vex_ast.registry.signature import VexFunctionSignature
from vex_ast.registry.categories import VexCategory, BehaviorType

# Create and register custom function
custom_signature = VexFunctionSignature(
    name="custom_function",
    category=VexCategory.UTILITY,
    behavior=BehaviorType.CONTROL,
    # ... other parameters
)

registry.register_function(custom_signature)
```

## Migration from Legacy Systems

If upgrading from older versions:

```python
# Old code (still works)
functions = registry_api.get_functions_by_simulation(SimulationCategory.MOTOR_CONTROL)

# Modern equivalent
functions = registry_api.get_functions_by_category_and_behavior(
    VexCategory.MOTOR, 
    BehaviorType.CONTROL
)
```