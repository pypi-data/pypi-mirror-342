"""
JSON serialization for AST nodes.

This module provides functionality to convert AST nodes to JSON format.
"""

import json
from typing import Any, Dict, List, Optional, Union, cast

from ..ast.interfaces import IAstNode
from ..visitors.base import AstVisitor
from ..utils.source_location import SourceLocation


class SerializationVisitor(AstVisitor[Dict[str, Any]]):
    """
    Visitor that converts AST nodes to dictionary representations.
    
    This visitor traverses the AST and converts each node to a dictionary
    that can be serialized to JSON. The dictionaries include node type
    information and all relevant attributes.
    """
    
    def generic_visit(self, node: IAstNode) -> Dict[str, Any]:
        """
        Default serialization logic for all node types.
        
        Args:
            node: The AST node to serialize
            
        Returns:
            A dictionary representation of the node
        """
        # Get the node's class name for type information
        node_type = node.__class__.__name__
        
        # Start with basic node information
        result = {
            "type": node_type,
        }
        
        # Add source location if available
        if node.location:
            result["location"] = self._serialize_location(node.location)
        
        # Add all attributes from the node
        attributes = node.get_attributes()
        for name, value in attributes.items():
            # Skip internal attributes and parent reference
            if name.startswith('_'):
                continue
                
            # Handle different attribute types
            result[name] = self._serialize_attribute(value)
            
        return result
    
    def _serialize_location(self, location: SourceLocation) -> Dict[str, Any]:
        """
        Serialize a source location to a dictionary.
        
        Args:
            location: The source location to serialize
            
        Returns:
            A dictionary representation of the source location
        """
        result = {
            "line": location.line,
            "column": location.column,
        }
        
        if location.end_line is not None:
            result["end_line"] = location.end_line
            
        if location.end_column is not None:
            result["end_column"] = location.end_column
            
        if location.filename:
            result["filename"] = location.filename
            
        return result
    
    def _serialize_attribute(self, value: Any) -> Any:
        """
        Serialize an attribute value based on its type.
        
        Args:
            value: The attribute value to serialize
            
        Returns:
            A serialized representation of the value
        """
        # Handle None
        if value is None:
            return None
            
        # Handle AST nodes
        if isinstance(value, IAstNode):
            return self.visit(value)
            
        # Handle lists of values
        if isinstance(value, list):
            return [self._serialize_attribute(item) for item in value]
            
        # Handle dictionaries
        if isinstance(value, dict):
            return {k: self._serialize_attribute(v) for k, v in value.items()}
            
        # Handle basic types (strings, numbers, booleans)
        if isinstance(value, (str, int, float, bool)):
            return value
            
        # Handle Operator enum values
        if hasattr(value, '__module__') and 'operators' in value.__module__ and hasattr(value, 'value'):
            return value.value
            
        # For other types, convert to string
        return str(value)


def serialize_ast_to_dict(ast: IAstNode) -> Dict[str, Any]:
    """
    Convert an AST node to a dictionary representation.
    
    Args:
        ast: The AST node to serialize
        
    Returns:
        A dictionary representation of the AST
    """
    visitor = SerializationVisitor()
    return visitor.visit(ast)


def serialize_ast_to_json(ast: IAstNode, indent: Optional[int] = None) -> str:
    """
    Convert an AST node to a JSON string.
    
    Args:
        ast: The AST node to serialize
        indent: Optional indentation level for pretty-printing
        
    Returns:
        A JSON string representation of the AST
    """
    data = serialize_ast_to_dict(ast)
    return json.dumps(data, indent=indent)
