# vex_ast/utils/type_definitions.py
"""Type definitions for type hints in the VEX AST."""

from typing import Any, Dict, List, Optional, TypeVar, Union, Type, Protocol

# Type variables for type hints
NodeType = TypeVar('NodeType')
VisitorType = TypeVar('VisitorType')
TransformerType = TypeVar('TransformerType')