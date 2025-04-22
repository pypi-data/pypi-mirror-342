# VEX AST Package

The VEX AST (Abstract Syntax Tree) package provides a comprehensive framework for parsing, analyzing, and simulating VEX V5 Robot Python code.

## Key Features

### Advanced Registry System
- Dual-axis categorization (Category × Behavior)
- Intelligent function signature validation
- Language mapping (Python ↔ C++)
- Full backward compatibility

### Robust AST Generation
- Python 3.8+ parsing with modern features
- VEX-specific node types
- Source location tracking
- Error recovery and reporting

### Extensible Visitor Pattern
- Analysis visitors (NodeCounter, VariableCollector)
- Transformation capabilities
- Pretty printing and serialization

## What's New in 0.2.6

### Unified Category System
- Introduced `VexCategory` enum for component types
- Added `BehaviorType` enum for function behaviors
- Maintained `SubCategory` for detailed classification
- Deprecated `SimulationCategory` (still supported)

### Enhanced Registry API
- New query methods for behavior-based lookups
- Combined category/behavior queries
- Improved validation logic

### Missing Components Added
- Brain and Controller constructors
- Complete VEX object type coverage

## Usage

### Basic Parsing
```python
from vex_ast import parse_string

code = """
motor1 = Motor(PORT1)
motor1.spin(FORWARD, 50, RPM)
"""

ast = parse_string(code)
```

### Registry Access
```python
from vex_ast.registry.api import registry_api
from vex_ast.registry.categories import VexCategory, BehaviorType

# Find control functions
control_funcs = registry_api.get_functions_by_behavior(BehaviorType.CONTROL)

# Find motor functions
motor_funcs = registry_api.get_functions_by_category(VexCategory.MOTOR)
```

## Architecture Overview

```
vex_ast/
├── ast/          # AST node definitions
├── parser/       # Parsing logic
├── registry/     # Function registry system
│   ├── api.py    # Public API
│   ├── categories.py  # Category system
│   └── functions/     # Function definitions
├── types/        # Type system
├── utils/        # Utilities
└── visitors/     # AST traversal
```

## Installation

```bash
pip install vex-ast
```

## Documentation

- [API Reference](./READMEAPI.md)
- [Registry Guide](./registry/README.md)
- [Type System](./types/README.md)
- [Visitor Pattern](./visitors/README.md)

## Contributing

We welcome contributions! Please see our contributing guidelines and code of conduct.

## License

HX2's Vex AST © 2025 by charkwayteowy is licensed under CC BY-NC 4.0