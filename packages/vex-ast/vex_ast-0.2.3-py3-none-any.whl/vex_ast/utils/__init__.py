"""
Utilities package for VEX AST.

This package provides utility functions and classes for working with the AST.
"""

from .errors import (
    ErrorHandler,
    ErrorType,
    VexSyntaxError,
    VexAstError,
    Error
)
from .source_location import (
    SourceLocation,
)
from .type_definitions import (
    NodeType,
    VisitorType,
    TransformerType
)

__all__ = [
    # Error handling
    "ErrorHandler",
    "ErrorType",
    "VexSyntaxError",
    "VexAstError",
    "Error",
    
    # Source location
    "SourceLocation",
    
    # Type definitions
    "NodeType",
    "VisitorType",
    "TransformerType"
]