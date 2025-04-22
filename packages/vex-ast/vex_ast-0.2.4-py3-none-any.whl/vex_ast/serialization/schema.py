"""
JSON Schema generation for AST nodes.

This module provides functionality to generate JSON Schema definitions
for the AST structure, which can be used for validation and documentation.
"""

import json
import os
from typing import Any, Dict, List, Optional, Set, Type

from ..ast.core import Program, Expression, Statement
from ..ast.expressions import (
    AttributeAccess, BinaryOperation, FunctionCall, Identifier, KeywordArgument, 
    UnaryOperation, VariableReference
)
from ..ast.literals import (
    BooleanLiteral, NoneLiteral, NumberLiteral, StringLiteral
)
from ..ast.statements import (
    Assignment, BreakStatement, ContinueStatement, ExpressionStatement,
    ForLoop, FunctionDefinition, IfStatement, ReturnStatement, WhileLoop, Argument
)
from ..ast.vex_nodes import (
    DisplayOutput, MotorControl, SensorReading, TimingControl, VexAPICall
)


def generate_ast_schema() -> Dict[str, Any]:
    """
    Generate a JSON Schema describing the AST node structure.
    
    Returns:
        A JSON Schema object as a dictionary
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "VEX AST Schema",
        "description": "JSON Schema for VEX AST nodes",
        "type": "object",
        "required": ["type"],
        "properties": {
            "type": {
                "type": "string",
                "description": "The type of AST node"
            },
            "location": {
                "$ref": "#/definitions/SourceLocation"
            }
        },
        "oneOf": [
            {"$ref": f"#/definitions/{node_type}"} 
            for node_type in _get_all_node_types()
        ],
        "definitions": _generate_definitions()
    }
    
    return schema


def _get_all_node_types() -> List[str]:
    """
    Get a list of all AST node type names.
    
    Returns:
        A list of node type names
    """
    # Core types
    node_types = ["Program"]
    
    # Expression types
    node_types.extend([
        "Identifier", "VariableReference", "AttributeAccess",
        "BinaryOperation", "UnaryOperation", "FunctionCall",
        "KeywordArgument"
    ])
    
    # Literal types
    node_types.extend([
        "NumberLiteral", "StringLiteral", "BooleanLiteral", "NoneLiteral"
    ])
    
    # Statement types
    node_types.extend([
        "ExpressionStatement", "Assignment", "IfStatement",
        "WhileLoop", "ForLoop", "FunctionDefinition", "Argument",
        "ReturnStatement", "BreakStatement", "ContinueStatement"
    ])
    
    # VEX-specific types
    node_types.extend([
        "VexAPICall", "MotorControl", "SensorReading",
        "TimingControl", "DisplayOutput"
    ])
    
    return node_types


def _generate_definitions() -> Dict[str, Any]:
    """
    Generate schema definitions for all AST node types.
    
    Returns:
        A dictionary of schema definitions
    """
    definitions = {}
    
    # Add SourceLocation definition
    definitions["SourceLocation"] = {
        "type": "object",
        "required": ["line", "column"],
        "properties": {
            "line": {
                "type": "integer",
                "description": "The line number (1-based)"
            },
            "column": {
                "type": "integer",
                "description": "The column number (1-based)"
            },
            "end_line": {
                "type": "integer",
                "description": "The ending line number"
            },
            "end_column": {
                "type": "integer",
                "description": "The ending column number"
            },
            "filename": {
                "type": "string",
                "description": "The source filename"
            }
        }
    }
    
    # Add node type definitions
    
    # Program
    definitions["Program"] = {
        "type": "object",
        "required": ["type", "body"],
        "properties": {
            "type": {"enum": ["Program"]},
            "body": {
                "type": "array",
                "description": "List of statements in the program",
                "items": {"$ref": "#/definitions/Statement"}
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    # Expression base
    definitions["Expression"] = {
        "type": "object",
        "required": ["type"],
        "properties": {
            "type": {"type": "string"},
            "location": {"$ref": "#/definitions/SourceLocation"}
        },
        "oneOf": [
            {"$ref": f"#/definitions/{expr_type}"} 
            for expr_type in [
                "Identifier", "VariableReference", "AttributeAccess",
                "BinaryOperation", "UnaryOperation", "FunctionCall",
                "NumberLiteral", "StringLiteral", "BooleanLiteral", "NoneLiteral"
            ]
        ]
    }
    
    # Statement base
    definitions["Statement"] = {
        "type": "object",
        "required": ["type"],
        "properties": {
            "type": {"type": "string"},
            "location": {"$ref": "#/definitions/SourceLocation"}
        },
        "oneOf": [
            {"$ref": f"#/definitions/{stmt_type}"} 
            for stmt_type in [
                "ExpressionStatement", "Assignment", "IfStatement",
                "WhileLoop", "ForLoop", "FunctionDefinition",
                "ReturnStatement", "BreakStatement", "ContinueStatement"
            ]
        ]
    }
    
    # Literals
    definitions["NumberLiteral"] = {
        "type": "object",
        "required": ["type", "value"],
        "properties": {
            "type": {"enum": ["NumberLiteral"]},
            "value": {
                "oneOf": [
                    {"type": "number"},
                    {"type": "integer"}
                ],
                "description": "The numeric value"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["StringLiteral"] = {
        "type": "object",
        "required": ["type", "value"],
        "properties": {
            "type": {"enum": ["StringLiteral"]},
            "value": {
                "type": "string",
                "description": "The string value"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["BooleanLiteral"] = {
        "type": "object",
        "required": ["type", "value"],
        "properties": {
            "type": {"enum": ["BooleanLiteral"]},
            "value": {
                "type": "boolean",
                "description": "The boolean value"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["NoneLiteral"] = {
        "type": "object",
        "required": ["type"],
        "properties": {
            "type": {"enum": ["NoneLiteral"]},
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    # Expressions
    definitions["Identifier"] = {
        "type": "object",
        "required": ["type", "name"],
        "properties": {
            "type": {"enum": ["Identifier"]},
            "name": {
                "type": "string",
                "description": "The identifier name"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["VariableReference"] = {
        "type": "object",
        "required": ["type", "identifier"],
        "properties": {
            "type": {"enum": ["VariableReference"]},
            "identifier": {
                "$ref": "#/definitions/Identifier",
                "description": "The referenced identifier"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["AttributeAccess"] = {
        "type": "object",
        "required": ["type", "object", "attribute"],
        "properties": {
            "type": {"enum": ["AttributeAccess"]},
            "object": {
                "$ref": "#/definitions/Expression",
                "description": "The object expression"
            },
            "attribute": {
                "type": "string",
                "description": "The attribute name"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["BinaryOperation"] = {
        "type": "object",
        "required": ["type", "left", "op", "right"],
        "properties": {
            "type": {"enum": ["BinaryOperation"]},
            "left": {
                "$ref": "#/definitions/Expression",
                "description": "The left operand"
            },
            "op": {
                "type": "string",
                "description": "The operator"
            },
            "right": {
                "$ref": "#/definitions/Expression",
                "description": "The right operand"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["UnaryOperation"] = {
        "type": "object",
        "required": ["type", "op", "operand"],
        "properties": {
            "type": {"enum": ["UnaryOperation"]},
            "op": {
                "type": "string",
                "description": "The operator"
            },
            "operand": {
                "$ref": "#/definitions/Expression",
                "description": "The operand"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["FunctionCall"] = {
        "type": "object",
        "required": ["type", "function", "args"],
        "properties": {
            "type": {"enum": ["FunctionCall"]},
            "function": {
                "$ref": "#/definitions/Expression",
                "description": "The function expression"
            },
            "args": {
                "type": "array",
                "description": "The positional arguments",
                "items": {"$ref": "#/definitions/Expression"}
            },
            "keywords": {
                "type": "array",
                "description": "The keyword arguments",
                "items": {"$ref": "#/definitions/KeywordArgument"}
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["KeywordArgument"] = {
        "type": "object",
        "required": ["type", "name", "value"],
        "properties": {
            "type": {"enum": ["KeywordArgument"]},
            "name": {
                "type": "string",
                "description": "The argument name"
            },
            "value": {
                "$ref": "#/definitions/Expression",
                "description": "The argument value"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    # Statements
    definitions["ExpressionStatement"] = {
        "type": "object",
        "required": ["type", "expression"],
        "properties": {
            "type": {"enum": ["ExpressionStatement"]},
            "expression": {
                "$ref": "#/definitions/Expression",
                "description": "The expression"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["Assignment"] = {
        "type": "object",
        "required": ["type", "target", "value"],
        "properties": {
            "type": {"enum": ["Assignment"]},
            "target": {
                "$ref": "#/definitions/Expression",
                "description": "The assignment target"
            },
            "value": {
                "$ref": "#/definitions/Expression",
                "description": "The assigned value"
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    definitions["IfStatement"] = {
        "type": "object",
        "required": ["type", "test", "body"],
        "properties": {
            "type": {"enum": ["IfStatement"]},
            "test": {
                "$ref": "#/definitions/Expression",
                "description": "The condition expression"
            },
            "body": {
                "type": "array",
                "description": "The if-body statements",
                "items": {"$ref": "#/definitions/Statement"}
            },
            "orelse": {
                "oneOf": [
                    {
                        "type": "array",
                        "description": "The else-body statements",
                        "items": {"$ref": "#/definitions/Statement"}
                    },
                    {
                        "$ref": "#/definitions/IfStatement",
                        "description": "An elif statement"
                    }
                ]
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    # Add more definitions for other node types...
    
    # VEX-specific nodes
    definitions["VexAPICall"] = {
        "type": "object",
        "required": ["type", "function", "args"],
        "properties": {
            "type": {"enum": ["VexAPICall"]},
            "function": {
                "$ref": "#/definitions/Expression",
                "description": "The function expression"
            },
            "args": {
                "type": "array",
                "description": "The positional arguments",
                "items": {"$ref": "#/definitions/Expression"}
            },
            "keywords": {
                "type": "array",
                "description": "The keyword arguments",
                "items": {"$ref": "#/definitions/KeywordArgument"}
            },
            "location": {"$ref": "#/definitions/SourceLocation"}
        }
    }
    
    # Add more VEX-specific node definitions...
    
    return definitions


def export_schema_to_file(schema: Dict[str, Any], filepath: str, indent: int = 2) -> None:
    """
    Save the schema to a file.
    
    Args:
        schema: The schema to save
        filepath: The path to save the schema to
        indent: The indentation level for pretty-printing
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    # Write the schema to the file
    with open(filepath, 'w') as f:
        json.dump(schema, f, indent=indent)
