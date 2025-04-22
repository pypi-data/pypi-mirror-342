"""
Parser package for VEX AST.

This package provides functionality for parsing VEX code into an Abstract Syntax Tree.
"""

from .interfaces import (
    IParser,
    BaseParser
)
from .factory import NodeFactory, default_factory
from .python_parser import parse_string, parse_file, PythonParser

__all__ = [
    # Interfaces
    "IParser",
    "BaseParser",
    
    # Factory
    "NodeFactory",
    "default_factory",
    
    # Python parser
    "parse_string",
    "parse_file",
    "PythonParser"
]