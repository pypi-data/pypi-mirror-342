"""
Comprehensive integration tests for the vex_ast package.

These tests ensure that all API endpoints work together correctly in various scenarios.
"""

import os
import json
import tempfile
import pytest
from typing import Dict, Any

from vex_ast import (
    parse_string,
    parse_file,
    ErrorHandler,
    VexSyntaxError,
    VexAstError,
    PrintVisitor,
    NodeCounter,
    VariableCollector,
    create_navigator,
    serialize_ast_to_dict,
    serialize_ast_to_json,
    deserialize_ast_from_dict,
    deserialize_ast_from_json,
    generate_ast_schema,
    export_schema_to_file,
    registry_api
)
from vex_ast.ast.vex_nodes import VexAPICall
from vex_ast.ast.validators import validate_vex_functions


class TestComprehensiveIntegration:
    """Comprehensive integration tests for the vex_ast package."""

    def test_parse_file_functionality(self):
        """Test the parse_file functionality with a temporary file."""
        # Create a temporary file with VEX code
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
            temp_file.write("""
            # Define a motor
            motor1 = Motor(PORT1)
            
            # Define a function
            def move_forward(speed):
                motor1.spin(FORWARD, speed, PERCENT)
                wait(1, SECONDS)
                motor1.stop()
                return True
            
            # Call the function
            success = move_forward(50)
            """)
            temp_file_path = temp_file.name
        
        try:
            # Parse the file
            ast = parse_file(temp_file_path)
            
            # Verify the AST structure
            assert ast is not None
            assert len(ast.body) > 0
            
            # Find function definitions
            func_defs = [node for node in ast.body if node.__class__.__name__ == "FunctionDefinition"]
            assert len(func_defs) == 1
            assert func_defs[0].name == "move_forward"
            
            # Test that visitors work with the parsed AST
            printer = PrintVisitor()
            result = printer.visit(ast)
            assert isinstance(result, str)
            assert len(result) > 0
            
            counter = NodeCounter()
            count = counter.visit(ast)
            assert count > 10
            
            collector = VariableCollector()
            variables = collector.visit(ast)
            assert "motor1" in variables
            assert "speed" in variables
            
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

    def test_error_handling_integration(self):
        """Test error handling integration with parsing and visitors."""
        # Create an error handler that doesn't raise exceptions
        error_handler = ErrorHandler(raise_on_error=False)
        
        # Parse code with syntax errors
        code_with_errors = """
        def invalid_function(
            # Missing closing parenthesis
            print("This will cause an error")
        """
        
        # This should not raise an exception due to raise_on_error=False
        ast = parse_string(code_with_errors, error_handler=error_handler)
        
        # Verify that errors were collected
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) > 0
        
        # Try with a different error handler that raises exceptions
        error_handler_strict = ErrorHandler(raise_on_error=True)
        
        # This should raise a VexSyntaxError
        with pytest.raises(VexSyntaxError):
            parse_string(code_with_errors, error_handler=error_handler_strict)
        
        # Test error handling with valid code but invalid VEX API calls
        invalid_vex_code = """
        motor1 = Motor(PORT1)
        # Invalid: wrong arguments to spin
        motor1.spin(INVALID_DIRECTION, "not_a_number", "not_a_unit")
        """
        
        # Parse the code (should succeed syntactically)
        ast = parse_string(invalid_vex_code)
        
        # Validate VEX functions (should find errors)
        validation_errors = validate_vex_functions(ast)
        assert len(validation_errors) > 0

    def test_end_to_end_workflow(self):
        """Test an end-to-end workflow combining multiple API functions."""
        # 1. Parse a complex program
        code = """
        # Initialize motors
        left_motor = Motor(PORT1)
        right_motor = Motor(PORT2)
        
        # Define a function to drive forward
        def drive_forward(speed, time_ms):
            # Set both motors to the specified speed
            left_motor.set_velocity(speed, PERCENT)
            right_motor.set_velocity(speed, PERCENT)
            
            # Start the motors
            left_motor.spin(FORWARD)
            right_motor.spin(FORWARD)
            
            # Wait for the specified time
            wait(time_ms, MSEC)
            
            # Stop the motors
            left_motor.stop()
            right_motor.stop()
            
            return True
        
        # Define a function to turn
        def turn(direction, speed, angle):
            if direction == LEFT:
                left_motor.set_velocity(-speed, PERCENT)
                right_motor.set_velocity(speed, PERCENT)
            else:
                left_motor.set_velocity(speed, PERCENT)
                right_motor.set_velocity(-speed, PERCENT)
                
            left_motor.spin(FORWARD)
            right_motor.spin(FORWARD)
            
            # Wait until the robot has turned the specified angle
            wait_until(gyro.rotation() >= angle)
            
            left_motor.stop()
            right_motor.stop()
            
            return True
        
        # Main program
        def main():
            # Display welcome message
            brain.screen.print("Robot starting...")
            wait(1, SECONDS)
            
            # Drive forward at 50% speed for 2 seconds
            success = drive_forward(50, 2000)
            
            if success:
                # Turn right 90 degrees
                turn(RIGHT, 30, 90)
                
                # Drive forward again
                drive_forward(50, 1000)
                
                brain.screen.print("Mission completed!")
            else:
                brain.screen.print("Drive failed!")
            
            return 0
        """
        
        # 2. Parse the code
        ast = parse_string(code)
        
        # 3. Use a visitor to analyze the AST
        counter = NodeCounter()
        node_count = counter.visit(ast)
        assert node_count > 50  # Complex program should have many nodes
        
        # 4. Use the navigator to find specific nodes
        navigator = create_navigator(ast)
        
        # Find all function definitions
        func_defs = navigator.find_function_definitions()
        assert len(func_defs) == 3
        func_names = [func.name for func in func_defs]
        assert "drive_forward" in func_names
        assert "turn" in func_names
        assert "main" in func_names
        
        # Find all VEX API calls
        vex_calls = navigator.find_vex_api_calls()
        assert len(vex_calls) > 5
        
        # 5. Serialize the AST to JSON
        json_str = serialize_ast_to_json(ast)
        assert isinstance(json_str, str)
        
        # 6. Deserialize back to an AST
        deserialized_ast = deserialize_ast_from_json(json_str)
        
        # 7. Verify the deserialized AST has the same structure
        deserialized_func_defs = [node for node in deserialized_ast.body 
                                 if node.__class__.__name__ == "FunctionDefinition"]
        assert len(deserialized_func_defs) == 3
        deserialized_func_names = [func.name for func in deserialized_func_defs]
        assert set(deserialized_func_names) == set(func_names)
        
        # 8. Use a visitor on the deserialized AST
        collector = VariableCollector()
        variables = collector.visit(deserialized_ast)
        assert "left_motor" in variables
        assert "right_motor" in variables
        assert "speed" in variables
        assert "direction" in variables

    def test_schema_export_functionality(self):
        """Test the schema export functionality."""
        # Generate the schema
        schema = generate_ast_schema()
        assert isinstance(schema, dict)
        
        # Export the schema to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # Export the schema
            export_schema_to_file(schema, temp_file_path)
            
            # Verify the file exists and contains valid JSON
            assert os.path.exists(temp_file_path)
            
            with open(temp_file_path, 'r') as f:
                loaded_schema = json.load(f)
            
            # Check that it's the same schema
            assert loaded_schema["$schema"] == schema["$schema"]
            assert "definitions" in loaded_schema
            assert set(loaded_schema["definitions"].keys()) == set(schema["definitions"].keys())
            
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_edge_cases(self):
        """Test edge cases in parsing and serialization."""
        # Test parsing an empty program
        empty_ast = parse_string("")
        assert empty_ast is not None
        assert len(empty_ast.body) == 0
        
        # Test parsing a program with only comments
        comments_ast = parse_string("# This is a comment\n# Another comment")
        assert comments_ast is not None
        assert len(comments_ast.body) == 0
        
        # Test parsing a program with unusual whitespace
        whitespace_code = """
        
        
        x    =    42
        
        
        y    =    x    +    10
        
        
        """
        whitespace_ast = parse_string(whitespace_code)
        assert whitespace_ast is not None
        assert len(whitespace_ast.body) == 2
        
        # Test serializing and deserializing an empty program
        empty_json = serialize_ast_to_json(empty_ast)
        deserialized_empty = deserialize_ast_from_json(empty_json)
        assert deserialized_empty is not None
        assert len(deserialized_empty.body) == 0
        
        # Test with a program containing all types of literals
        literals_code = """
        # Number literals
        int_val = 42
        float_val = 3.14
        
        # String literals
        str_val = "Hello, world!"
        str_val2 = 'Single quotes'
        
        # Boolean literals
        bool_val1 = True
        bool_val2 = False
        
        # None literal
        none_val = None
        """
        
        literals_ast = parse_string(literals_code)
        assert literals_ast is not None
        assert len(literals_ast.body) > 0
        
        # Serialize and deserialize
        literals_json = serialize_ast_to_json(literals_ast)
        deserialized_literals = deserialize_ast_from_json(literals_json)
        
        # Verify the literals were preserved
        collector = VariableCollector()
        variables = collector.visit(deserialized_literals)
        assert len(variables) == 0  # All are assignments, no references
