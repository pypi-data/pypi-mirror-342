"""
VEX AST Generator Package.

Provides tools for parsing VEX V5 code and generating an Abstract Syntax Tree (AST).
"""

# Core functionality
from .ast.core import Program
from .parser.python_parser import parse_string, parse_file

# AST Navigation
from .ast.navigator import AstNavigator, create_navigator

# Visitors
from .visitors.printer import PrintVisitor
from .visitors.analyzer import NodeCounter, VariableCollector

# Error handling
from .utils.errors import ErrorHandler, ErrorType, VexSyntaxError, VexAstError, Error

# Registry
from .registry.api import registry_api
from .registry import initialize

# Serialization
from .serialization.json_serializer import serialize_ast_to_dict, serialize_ast_to_json
from .serialization.json_deserializer import deserialize_ast_from_dict, deserialize_ast_from_json
from .serialization.schema import generate_ast_schema, export_schema_to_file

__version__ = "0.2.0"

# Initialize the registry with default functions
initialize()

__all__ = [
    # Core functionality
    "Program",
    "parse_string",
    "parse_file",
    
    # AST Navigation
    "AstNavigator",
    "create_navigator",
    
    # Visitors
    "PrintVisitor",
    "NodeCounter",
    "VariableCollector",
    
    # Error handling
    "ErrorHandler",
    "ErrorType",
    "VexSyntaxError",
    "VexAstError",
    "Error",
    
    # Registry
    "registry_api",
    "initialize",
    
    # Serialization
    "serialize_ast_to_dict",
    "serialize_ast_to_json",
    "deserialize_ast_from_dict",
    "deserialize_ast_from_json",
    "generate_ast_schema",
    "export_schema_to_file"
]