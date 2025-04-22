# VEX AST Generator

A Python package for generating Abstract Syntax Trees (ASTs) for VEX V5 Robot Python code.

## Project Goal

The primary goal of this project is to provide a robust and extensible framework for parsing VEX V5 Python code and representing it as an Abstract Syntax Tree (AST). This AST can then be used for various purposes, such as static analysis, code transformation, simulation, or integration with other development tools specific to the VEX ecosystem.

## Features (Implemented)

*   Parsing of standard Python syntax relevant to VEX programming.
*   Generation of a well-defined AST structure using custom node types.
*   Representation of core Python constructs (variables, functions, loops, conditionals, expressions).
*   Specific AST nodes for common VEX API patterns (e.g., `MotorControl`, `SensorReading`).
*   Visitor pattern implementation (`vex_ast.visitors`) for easy AST traversal and manipulation.
*   Basic analysis visitors (`NodeCounter`, `VariableCollector`).
*   AST pretty-printing visitor (`PrintVisitor`).
*   Error handling and reporting with source location information (`vex_ast.utils`).
*   JSON serialization and deserialization of AST nodes (`vex_ast.serialization`).
*   JSON Schema generation for AST structure validation and documentation.

## Library Structure

The core library is within the `vex_ast` directory:

*   `vex_ast/ast/`: Defines the structure and node types of the Abstract Syntax Tree.
*   `vex_ast/parser/`: Contains the logic for parsing Python source code into the AST.
*   `vex_ast/visitors/`: Provides tools for traversing and analyzing the generated AST.
*   `vex_ast/utils/`: Includes helper modules for error handling and source location tracking.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/vex_ast.git # Replace with actual URL
    cd vex_ast
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Install for development:**
    If you plan to contribute to the project, install it in editable mode along with development dependencies:
    ```bash
    pip install -e .[dev]
    ```

## Usage Example

### Basic Parsing and Printing

```python
from vex_ast import parse_string
from vex_ast.visitors.printer import PrintVisitor

# VEX-like Python code
code = """
left_motor = Motor("port1")
right_motor = Motor("port10")

def drive_forward(speed_percent):
    left_motor.spin(FORWARD, speed_percent, PERCENT)
    right_motor.spin(FORWARD, speed_percent, PERCENT)
    wait(1, SECONDS)
    left_motor.stop()
    right_motor.stop()

drive_forward(50)
print("Movement complete!")
"""

try:
    # Parse the code string into an AST
    ast_tree = parse_string(code)

    # Use the PrintVisitor to get a textual representation of the AST
    printer = PrintVisitor()
    ast_representation = printer.visit(ast_tree)

    print("--- AST Representation ---")
    print(ast_representation)

except Exception as e:
    print(f"An error occurred: {e}")
```

### Serialization and Deserialization

```python
from vex_ast import (
    parse_string, 
    serialize_ast_to_json, 
    deserialize_ast_from_json,
    export_schema_to_file
)

# Parse code into an AST
code = "x = 10 + 20"
ast = parse_string(code)

# Serialize the AST to JSON
json_str = serialize_ast_to_json(ast, indent=2)
print(json_str)

# Save the AST to a file
with open("ast.json", "w") as f:
    f.write(json_str)

# Later, load the AST from JSON
with open("ast.json", "r") as f:
    loaded_json = f.read()
    
# Deserialize back to an AST object
loaded_ast = deserialize_ast_from_json(loaded_json)

# Generate and export a JSON schema
export_schema_to_file("ast_schema.json")
```

## Development
```bash
Running Tests
pytest
```
```bash
Type Checking
mypy vex_ast
```
```bash
Formatting and Linting
black vex_ast tests
flake8 vex_ast tests
```
## Contributing

Contributions are welcome! Please follow the established coding standards and ensure tests pass before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details (You'll need to add a LICENSE file).
