"""
Tests for the serialization functionality.
"""

import json
import pytest
from typing import Dict, Any

from vex_ast import (
    parse_string, 
    serialize_ast_to_dict, 
    serialize_ast_to_json,
    deserialize_ast_from_dict,
    deserialize_ast_from_json,
    generate_ast_schema
)
from vex_ast.ast.core import Program
from vex_ast.ast.literals import NumberLiteral, StringLiteral, BooleanLiteral
from vex_ast.utils.source_location import SourceLocation


class TestSerialization:
    """Test cases for AST serialization and deserialization."""
    
    def test_serialize_simple_ast(self):
        """Test serializing a simple AST to a dictionary."""
        # Parse a simple program
        code = "x = 42"
        ast = parse_string(code)
        
        # Serialize to dictionary
        data = serialize_ast_to_dict(ast)
        
        # Basic checks
        assert isinstance(data, dict)
        assert data["type"] == "Program"
        assert "body" in data
        assert isinstance(data["body"], list)
        assert len(data["body"]) == 1
        
        # Check the assignment statement
        assignment = data["body"][0]
        assert assignment["type"] == "Assignment"
        assert assignment["target"]["type"] == "Identifier"
        assert assignment["target"]["name"] == "x"
        assert assignment["value"]["type"] == "NumberLiteral"
        assert assignment["value"]["value"] == 42
    
    def test_serialize_complex_ast(self):
        """Test serializing a more complex AST to a dictionary."""
        # Parse a more complex program
        code = """
        def calculate(a, b):
            result = a + b
            return result
            
        x = calculate(10, 20)
        if x > 25:
            print("Greater than 25")
        else:
            print("Less than or equal to 25")
        """
        ast = parse_string(code)
        
        # Serialize to dictionary
        data = serialize_ast_to_dict(ast)
        
        # Basic checks
        assert isinstance(data, dict)
        assert data["type"] == "Program"
        assert "body" in data
        assert isinstance(data["body"], list)
        assert len(data["body"]) == 3  # function def, assignment, if statement
        
        # Check function definition
        func_def = data["body"][0]
        assert func_def["type"] == "FunctionDefinition"
        assert func_def["name"] == "calculate"
        assert len(func_def["args"]) == 2
        
        # Check if statement
        if_stmt = data["body"][2]
        assert if_stmt["type"] == "IfStatement"
        assert if_stmt["test"]["type"] == "BinaryOperation"
        assert if_stmt["test"]["op"] == ">"
        assert "orelse" in if_stmt
    
    def test_serialize_to_json(self):
        """Test serializing an AST to JSON."""
        # Parse a simple program
        code = "x = 42"
        ast = parse_string(code)
        
        # Serialize to JSON
        json_str = serialize_ast_to_json(ast)
        
        # Check that it's valid JSON
        data = json.loads(json_str)
        assert isinstance(data, dict)
        assert data["type"] == "Program"
    
    def test_round_trip_serialization(self):
        """Test round-trip serialization (AST -> JSON -> AST)."""
        # Parse a program
        code = """
        x = 10
        y = 20
        result = x + y
        print(result)
        """
        original_ast = parse_string(code)
        
        # Serialize to JSON
        json_str = serialize_ast_to_json(original_ast)
        
        # Deserialize back to AST
        deserialized_ast = deserialize_ast_from_json(json_str)
        
        # Serialize both to dictionaries for comparison
        original_dict = serialize_ast_to_dict(original_ast)
        deserialized_dict = serialize_ast_to_dict(deserialized_ast)
        
        # Compare the dictionaries (excluding location info which might differ)
        self._compare_dicts_ignoring_location(original_dict, deserialized_dict)
    
    def test_deserialize_from_dict(self):
        """Test deserializing an AST from a dictionary."""
        # Create a dictionary representation manually
        data = {
            "type": "Program",
            "body": [
                {
                    "type": "Assignment",
                    "target": {
                        "type": "Identifier",
                        "name": "x"
                    },
                    "value": {
                        "type": "NumberLiteral",
                        "value": 42
                    }
                }
            ]
        }
        
        # Deserialize to AST
        ast = deserialize_ast_from_dict(data)
        
        # Check the AST structure
        assert isinstance(ast, Program)
        assert len(ast.body) == 1
        assert ast.body[0].target.name == "x"
        assert ast.body[0].value.value == 42
    
    def test_source_location_serialization(self):
        """Test that source location information is properly serialized."""
        # Create a node with source location
        location = SourceLocation(line=10, column=5, end_line=10, end_column=10)
        node = NumberLiteral(42, location)
        
        # Serialize to dictionary
        data = serialize_ast_to_dict(node)
        
        # Check location information
        assert "location" in data
        assert data["location"]["line"] == 10
        assert data["location"]["column"] == 5
        assert data["location"]["end_line"] == 10
        assert data["location"]["end_column"] == 10
    
    def test_schema_generation(self):
        """Test generating a JSON schema for the AST structure."""
        # Generate schema
        schema = generate_ast_schema()
        
        # Basic checks
        assert isinstance(schema, dict)
        assert "$schema" in schema
        assert "definitions" in schema
        
        # Check that core node types are defined
        definitions = schema["definitions"]
        assert "Program" in definitions
        assert "Expression" in definitions
        assert "Statement" in definitions
        assert "NumberLiteral" in definitions
        assert "StringLiteral" in definitions
        assert "IfStatement" in definitions
    
    def test_literal_serialization(self):
        """Test serialization of different literal types."""
        # Create literal nodes
        num_literal = NumberLiteral(42)
        str_literal = StringLiteral("hello")
        bool_literal = BooleanLiteral(True)
        
        # Serialize to dictionaries
        num_data = serialize_ast_to_dict(num_literal)
        str_data = serialize_ast_to_dict(str_literal)
        bool_data = serialize_ast_to_dict(bool_literal)
        
        # Check number literal
        assert num_data["type"] == "NumberLiteral"
        assert num_data["value"] == 42
        
        # Check string literal
        assert str_data["type"] == "StringLiteral"
        assert str_data["value"] == "hello"
        
        # Check boolean literal
        assert bool_data["type"] == "BooleanLiteral"
        assert bool_data["value"] is True
    
    def test_special_characters_in_strings(self):
        """Test handling of special characters in string literals."""
        # Create a string with special characters
        special_str = "Line 1\nLine 2\tTabbed\u2022 Unicode"
        node = StringLiteral(special_str)
        
        # Serialize and deserialize
        json_str = serialize_ast_to_json(node)
        deserialized = deserialize_ast_from_json(json_str)
        
        # Check the value was preserved
        assert deserialized.value == special_str
    
    def test_to_dict_method(self):
        """Test the to_dict method added to IAstNode."""
        # Parse a simple program
        code = "x = 42"
        ast = parse_string(code)
        
        # Use the to_dict method
        data = ast.to_dict()
        
        # Check the result
        assert isinstance(data, dict)
        assert data["type"] == "Program"
        assert "body" in data
    
    def _compare_dicts_ignoring_location(self, dict1: Dict[str, Any], dict2: Dict[str, Any]):
        """
        Compare two dictionaries, ignoring 'location' fields.
        
        Args:
            dict1: First dictionary
            dict2: Second dictionary
        """
        # Check types
        assert dict1["type"] == dict2["type"]
        
        # Compare other fields
        for key in dict1:
            if key == "location":
                continue
                
            if key not in dict2:
                pytest.fail(f"Key '{key}' missing from second dictionary")
                
            value1 = dict1[key]
            value2 = dict2[key]
            
            if isinstance(value1, dict) and isinstance(value2, dict):
                self._compare_dicts_ignoring_location(value1, value2)
            elif isinstance(value1, list) and isinstance(value2, list):
                assert len(value1) == len(value2)
                for item1, item2 in zip(value1, value2):
                    if isinstance(item1, dict) and isinstance(item2, dict):
                        self._compare_dicts_ignoring_location(item1, item2)
                    else:
                        assert item1 == item2
            else:
                assert value1 == value2
