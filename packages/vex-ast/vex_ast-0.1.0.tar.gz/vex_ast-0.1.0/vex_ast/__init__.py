"""
VEX AST Generator Package.

Provides tools for parsing VEX V5 code and generating an Abstract Syntax Tree (AST).
"""

from .ast.core import Program
from .ast.navigator import AstNavigator
from .parser.python_parser import parse_string, parse_file
from .visitors.printer import PrintVisitor
from .visitors.analyzer import NodeCounter, VariableCollector
from .utils.errors import ErrorHandler, ErrorType, VexSyntaxError
from .registry import registry_api, initialize as initialize_registry
from .serialization.json_serializer import serialize_ast_to_dict, serialize_ast_to_json
from .serialization.json_deserializer import deserialize_ast_from_dict, deserialize_ast_from_json
from .serialization.schema import generate_ast_schema, export_schema_to_file

__version__ = "0.2.0"

# Initialize the registry with default functions
initialize_registry()

def create_navigator(ast: Program) -> AstNavigator:
    """Create an AST navigator for the given AST.
    
    Args:
        ast: The AST to navigate
        
    Returns:
        An AST navigator for traversing and querying the AST
    """
    return AstNavigator(ast)

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
    
    # Registry
    "registry_api",
    "initialize_registry",
    
    # Serialization
    "serialize_ast_to_dict",
    "serialize_ast_to_json",
    "deserialize_ast_from_dict",
    "deserialize_ast_from_json",
    "generate_ast_schema",
    "export_schema_to_file"
]
