"""
JSON deserialization for AST nodes.

This module provides functionality to convert JSON data back to AST nodes.
"""

import json
from typing import Any, Dict, List, Optional, Type, Union, cast

from ..ast.interfaces import IAstNode
from ..parser.factory import NodeFactory
from ..utils.source_location import SourceLocation
from ..utils.errors import ErrorHandler, ErrorType


class DeserializationFactory:
    """
    Factory for deserializing JSON data back to AST nodes.
    
    This class uses the NodeFactory to create AST nodes from serialized data,
    handling the reconstruction of the node hierarchy and parent-child relationships.
    """
    
    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        """
        Initialize the deserialization factory.
        
        Args:
            error_handler: Optional error handler for reporting deserialization issues
        """
        self.node_factory = NodeFactory(error_handler)
        self.error_handler = error_handler
    
    def deserialize_node(self, data: Dict[str, Any]) -> IAstNode:
        """
        Deserialize a dictionary representation back to an AST node.
        
        Args:
            data: Dictionary representation of an AST node
            
        Returns:
            The reconstructed AST node
            
        Raises:
            ValueError: If the data is invalid or missing required fields
        """
        # Extract node type
        if "type" not in data:
            raise ValueError("Missing 'type' field in node data")
            
        node_type = data["type"]
        
        # Create source location if present
        location = None
        if "location" in data:
            location = self._deserialize_location(data["location"])
        
        # Dispatch to appropriate creation method based on node type
        method_name = f"_create_{node_type.lower()}"
        if hasattr(self, method_name):
            create_method = getattr(self, method_name)
            node = create_method(data, location)
        else:
            # Fallback to generic creation if no specific method exists
            node = self._create_generic_node(node_type, data, location)
            
        return node
    
    def _deserialize_location(self, data: Dict[str, Any]) -> SourceLocation:
        """
        Deserialize a dictionary to a SourceLocation object.
        
        Args:
            data: Dictionary representation of a source location
            
        Returns:
            A SourceLocation object
        """
        return SourceLocation(
            line=data["line"],
            column=data["column"],
            end_line=data.get("end_line"),
            end_column=data.get("end_column"),
            filename=data.get("filename")
        )
    
    def _deserialize_value(self, value: Any) -> Any:
        """
        Deserialize a value based on its type.
        
        Args:
            value: The value to deserialize
            
        Returns:
            The deserialized value
        """
        # Handle None
        if value is None:
            return None
            
        # Handle dictionaries (potentially nested nodes)
        if isinstance(value, dict) and "type" in value:
            return self.deserialize_node(value)
            
        # Handle lists of values
        if isinstance(value, list):
            return [self._deserialize_value(item) for item in value]
            
        # Handle dictionaries (not nodes)
        if isinstance(value, dict):
            return {k: self._deserialize_value(v) for k, v in value.items()}
            
        # Return basic types as-is
        return value
    
    def _create_generic_node(self, node_type: str, data: Dict[str, Any], 
                            location: Optional[SourceLocation]) -> IAstNode:
        """
        Generic node creation when no specific method exists.
        
        Args:
            node_type: The type of node to create
            data: Dictionary representation of the node
            location: Optional source location
            
        Returns:
            The created AST node
            
        Raises:
            ValueError: If the node type is not supported
        """
        # Map of node types to factory methods
        factory_methods = {
            # Literals
            "NumberLiteral": self.node_factory.create_number_literal,
            "StringLiteral": self.node_factory.create_string_literal,
            "BooleanLiteral": self.node_factory.create_boolean_literal,
            "NoneLiteral": self.node_factory.create_none_literal,
            
            # Expressions
            "Identifier": self.node_factory.create_identifier,
            "VariableReference": self.node_factory.create_variable_reference,
            "AttributeAccess": self.node_factory.create_attribute_access,
            "BinaryOperation": self.node_factory.create_binary_operation,
            "UnaryOperation": self.node_factory.create_unary_operation,
            "ConditionalExpression": self.node_factory.create_conditional_expression,
            "FunctionCall": self.node_factory.create_function_call,
            "KeywordArgument": self.node_factory.create_keyword_argument,
            
            # Statements
            "ExpressionStatement": self.node_factory.create_expression_statement,
            "Assignment": self.node_factory.create_assignment,
            "IfStatement": self.node_factory.create_if_statement,
            "WhileLoop": self.node_factory.create_while_loop,
            "ForLoop": self.node_factory.create_for_loop,
            "FunctionDefinition": self.node_factory.create_function_definition,
            "Argument": self.node_factory.create_argument,
            "ReturnStatement": self.node_factory.create_return_statement,
            "BreakStatement": self.node_factory.create_break_statement,
            "ContinueStatement": self.node_factory.create_continue_statement,
            
            # VEX-specific nodes
            "VexAPICall": self.node_factory.create_vex_api_call,
            "MotorControl": self.node_factory.create_motor_control,
            "SensorReading": self.node_factory.create_sensor_reading,
            "TimingControl": self.node_factory.create_timing_control,
            "DisplayOutput": self.node_factory.create_display_output,
            
            # Core
            "Program": self.node_factory.create_program,
        }
        
        if node_type not in factory_methods:
            raise ValueError(f"Unsupported node type: {node_type}")
            
        # Extract and deserialize attributes
        kwargs = {}
        for key, value in data.items():
            if key not in ["type", "location"]:
                kwargs[key] = self._deserialize_value(value)
                
        # Create the node using the appropriate factory method
        factory_method = factory_methods[node_type]
        
        # Special handling for certain node types
        if node_type == "Program":
            return factory_method(kwargs.get("body", []), location)
        elif node_type in ["NumberLiteral", "StringLiteral", "BooleanLiteral"]:
            return factory_method(kwargs.get("value"), location)
        elif node_type == "NoneLiteral":
            return factory_method(location)
        elif node_type == "Identifier":
            return factory_method(kwargs.get("name", ""), location)
        
        # For other node types, pass all kwargs and location
        # This is a simplified approach; in a real implementation,
        # you would need to handle each node type specifically
        try:
            return factory_method(**kwargs, location=location)
        except TypeError as e:
            # If the factory method doesn't accept the kwargs, report an error
            if self.error_handler:
                self.error_handler.add_error(
                    error_type=ErrorType.INTERNAL_ERROR,
                    message=f"Failed to create {node_type}: {str(e)}"
                )
            raise ValueError(f"Failed to deserialize {node_type}: {str(e)}")
    
    # Specific node creation methods for complex cases
    
    def _create_attributeaccess(self, data: Dict[str, Any],
                               location: Optional[SourceLocation]) -> IAstNode:
        """Create an AttributeAccess node from serialized data."""
        object_expr = self._deserialize_value(data.get("object"))
        attribute = data.get("attribute", "")
        return self.node_factory.create_attribute_access(object_expr, attribute, location)
    
    def _create_program(self, data: Dict[str, Any], 
                       location: Optional[SourceLocation]) -> IAstNode:
        """Create a Program node from serialized data."""
        body = [self._deserialize_value(stmt) for stmt in data.get("body", [])]
        return self.node_factory.create_program(body, location)
    
    def _create_functioncall(self, data: Dict[str, Any], 
                            location: Optional[SourceLocation]) -> IAstNode:
        """Create a FunctionCall node from serialized data."""
        function = self._deserialize_value(data.get("function"))
        args = [self._deserialize_value(arg) for arg in data.get("args", [])]
        keywords = [self._deserialize_value(kw) for kw in data.get("keywords", [])]
        return self.node_factory.create_function_call(function, args, keywords, location)
    
    def _create_conditionalexpression(self, data: Dict[str, Any],
                                     location: Optional[SourceLocation]) -> IAstNode:
        """Create a ConditionalExpression node from serialized data."""
        condition = self._deserialize_value(data.get("condition"))
        true_expr = self._deserialize_value(data.get("true_expr"))
        false_expr = self._deserialize_value(data.get("false_expr"))
        return self.node_factory.create_conditional_expression(condition, true_expr, false_expr, location)
    
    def _create_ifstatement(self, data: Dict[str, Any], 
                           location: Optional[SourceLocation]) -> IAstNode:
        """Create an IfStatement node from serialized data."""
        test = self._deserialize_value(data.get("test"))
        body = [self._deserialize_value(stmt) for stmt in data.get("body", [])]
        orelse = None
        if "orelse" in data:
            orelse_data = data["orelse"]
            if isinstance(orelse_data, list):
                orelse = [self._deserialize_value(stmt) for stmt in orelse_data]
            else:
                orelse = self._deserialize_value(orelse_data)
        return self.node_factory.create_if_statement(test, body, orelse, location)


def deserialize_ast_from_dict(data: Dict[str, Any], 
                             error_handler: Optional[ErrorHandler] = None) -> IAstNode:
    """
    Create an AST from a dictionary representation.
    
    Args:
        data: Dictionary representation of an AST
        error_handler: Optional error handler for reporting deserialization issues
        
    Returns:
        The reconstructed AST
    """
    factory = DeserializationFactory(error_handler)
    return factory.deserialize_node(data)


def deserialize_ast_from_json(json_str: str, 
                             error_handler: Optional[ErrorHandler] = None) -> IAstNode:
    """
    Create an AST from a JSON string.
    
    Args:
        json_str: JSON string representation of an AST
        error_handler: Optional error handler for reporting deserialization issues
        
    Returns:
        The reconstructed AST
    """
    data = json.loads(json_str)
    return deserialize_ast_from_dict(data, error_handler)
