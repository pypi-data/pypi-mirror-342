"""Literal value nodes for the AST."""

from typing import Any, List, Optional, Union

from .interfaces import IAstNode, IVisitor, T_VisitorResult, ILiteral
from .core import Expression
from ..utils.source_location import SourceLocation

class Literal(Expression, ILiteral):
    """Base class for all literal values."""
    
    _fields = ('value',)
    
    def __init__(self, value: Any, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.value = value
    
    def get_children(self) -> List[IAstNode]:
        """Literals have no children."""
        return []
    
    def get_value(self) -> Any:
        """Get the literal value."""
        return self.value

class NumberLiteral(Literal):
    """A numeric literal (integer or float)."""
    
    def __init__(self, value: Union[int, float], location: Optional[SourceLocation] = None):
        super().__init__(value, location)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_numberliteral(self)
    
    def is_integer(self) -> bool:
        """Check if this is an integer literal."""
        return isinstance(self.value, int)
    
    def is_float(self) -> bool:
        """Check if this is a float literal."""
        return isinstance(self.value, float)

class StringLiteral(Literal):
    """A string literal."""
    
    def __init__(self, value: str, location: Optional[SourceLocation] = None):
        super().__init__(value, location)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_stringliteral(self)
    
    def get_length(self) -> int:
        """Get the length of the string."""
        return len(self.value)

class BooleanLiteral(Literal):
    """A boolean literal (True or False)."""
    
    def __init__(self, value: bool, location: Optional[SourceLocation] = None):
        super().__init__(value, location)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_booleanliteral(self)
    
    def is_true(self) -> bool:
        """Check if this is a True literal."""
        return self.value is True
    
    def is_false(self) -> bool:
        """Check if this is a False literal."""
        return self.value is False

class NoneLiteral(Literal):
    """A None literal."""
    
    def __init__(self, location: Optional[SourceLocation] = None):
        super().__init__(None, location)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_noneliteral(self)
