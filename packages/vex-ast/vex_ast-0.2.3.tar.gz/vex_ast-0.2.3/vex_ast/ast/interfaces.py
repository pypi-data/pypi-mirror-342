"""Fundamental interfaces and protocols for the AST."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Optional, Protocol, TypeVar, Generic, runtime_checkable, Dict, Union, Tuple

from ..utils.source_location import SourceLocation

# Visitor pattern type variable
T_VisitorResult = TypeVar('T_VisitorResult')

class IVisitor(Protocol, Generic[T_VisitorResult]):
    """Protocol for AST visitors."""
    
    def visit(self, node: 'IAstNode') -> T_VisitorResult:
        """Visit an AST node."""
        ...

@runtime_checkable
class IAstNode(Protocol):
    """Protocol defining the minimum interface for an AST node."""
    
    location: Optional[SourceLocation]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        """Accept a visitor (Visitor Pattern)."""
        ...
    
    def get_children(self) -> Iterable['IAstNode']:
        """Get child nodes of this node."""
        ...
    
    def get_child_by_name(self, name: str) -> Optional['IAstNode']:
        """Get a child node by its field name."""
        ...
    
    def get_child_names(self) -> List[str]:
        """Get the names of all child fields."""
        ...
    
    def get_parent(self) -> Optional['IAstNode']:
        """Get the parent node, if available."""
        ...
    
    def get_attributes(self) -> Dict[str, Any]:
        """Get all attributes of this node as a dictionary."""
        ...
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary representation.
        
        This is an optional method for serialization support.
        
        Returns:
            A dictionary representation of the node
        """
        ...

@runtime_checkable
class IExpression(IAstNode, Protocol):
    """Protocol for expression nodes."""
    pass

@runtime_checkable
class IStatement(IAstNode, Protocol):
    """Protocol for statement nodes."""
    pass

@runtime_checkable
class ILiteral(IExpression, Protocol):
    """Protocol for literal value nodes."""
    value: Any
    
    def get_value(self) -> Any:
        """Get the literal value."""
        ...

@runtime_checkable
class IIdentifier(IExpression, Protocol):
    """Protocol for identifier nodes."""
    name: str
    
    def get_name(self) -> str:
        """Get the identifier name."""
        ...

@runtime_checkable
class IFunctionCall(IExpression, Protocol):
    """Protocol for function call nodes."""
    
    def get_function_expr(self) -> IExpression:
        """Get the function expression."""
        ...
    
    def get_arguments(self) -> List[IExpression]:
        """Get the positional arguments."""
        ...
    
    def get_keyword_arguments(self) -> Dict[str, IExpression]:
        """Get the keyword arguments as a dictionary."""
        ...

@runtime_checkable
class IAssignment(IStatement, Protocol):
    """Protocol for assignment nodes."""
    
    def get_target(self) -> IExpression:
        """Get the assignment target."""
        ...
    
    def get_value(self) -> IExpression:
        """Get the assigned value."""
        ...

class AstNode(ABC):
    """Abstract base implementation of the IAstNode protocol."""
    
    def __init__(self, location: Optional[SourceLocation] = None):
        self.location = location
        self._parent: Optional[IAstNode] = None
    
    @abstractmethod
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        """Accept a visitor (Visitor Pattern)."""
        pass
    
    @abstractmethod
    def get_children(self) -> List[IAstNode]:
        """Get child nodes of this node."""
        pass
    
    def get_child_by_name(self, name: str) -> Optional[IAstNode]:
        """Get a child node by its field name."""
        if not hasattr(self, '_fields') or name not in getattr(self, '_fields'):
            return None
        
        value = getattr(self, name, None)
        if isinstance(value, IAstNode):
            return value
        elif isinstance(value, list) and value and isinstance(value[0], IAstNode):
            return value[0]  # Return first item if it's a list of nodes
        
        return None
    
    def get_child_names(self) -> List[str]:
        """Get the names of all child fields."""
        if not hasattr(self, '_fields'):
            return []
        return list(getattr(self, '_fields'))
    
    def get_parent(self) -> Optional[IAstNode]:
        """Get the parent node, if available."""
        return getattr(self, '_parent', None)
    
    def set_parent(self, parent: IAstNode) -> None:
        """Set the parent node reference."""
        self._parent = parent
    
    def get_attributes(self) -> Dict[str, Any]:
        """Get all attributes of this node as a dictionary."""
        result = {}
        if hasattr(self, '_fields'):
            for field in getattr(self, '_fields'):
                result[field] = getattr(self, field, None)
        return result
    
    def __eq__(self, other: Any) -> bool:
        """Compare nodes for equality."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        
        # Compare all attributes defined in _fields
        if hasattr(self, '_fields'):
            for field in getattr(self, '_fields'):
                if getattr(self, field, None) != getattr(other, field, None):
                    return False
        
        # Compare location
        return self.location == other.location
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary representation.
        
        This implementation uses the serialization visitor to create a
        dictionary representation of the node.
        
        Returns:
            A dictionary representation of the node
        """
        from ..serialization.json_serializer import serialize_ast_to_dict
        return serialize_ast_to_dict(self)
