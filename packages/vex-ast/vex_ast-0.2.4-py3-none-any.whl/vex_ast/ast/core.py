"""Core AST node implementations."""

from typing import Any, Dict, List, Optional, Union, cast

from .interfaces import AstNode, IAstNode, IExpression, IStatement, IVisitor, T_VisitorResult
from ..utils.source_location import SourceLocation

class Expression(AstNode):
    """Base class for expression nodes."""
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        """Default implementation that defers to visitor."""
        method_name = f"visit_{self.__class__.__name__.lower()}"
        if hasattr(visitor, method_name):
            return getattr(visitor, method_name)(self)
        return visitor.visit_expression(self)

class Statement(AstNode):
    """Base class for statement nodes."""
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        """Default implementation that defers to visitor."""
        method_name = f"visit_{self.__class__.__name__.lower()}"
        if hasattr(visitor, method_name):
            return getattr(visitor, method_name)(self)
        return visitor.visit_statement(self)

class Program(AstNode):
    """Root node of the AST, representing the entire program."""
    
    _fields = ('body',)
    
    def __init__(self, body: List[IStatement], location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.body = body
        
        # Set parent references
        for statement in self.body:
            if isinstance(statement, AstNode):
                statement.set_parent(self)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        """Accept a visitor."""
        return visitor.visit_program(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return cast(List[IAstNode], self.body)
    
    def get_statements(self) -> List[IStatement]:
        """Get all statements in the program."""
        return self.body
    
    def add_statement(self, statement: IStatement) -> None:
        """Add a statement to the program."""
        self.body.append(statement)
        if isinstance(statement, AstNode):
            statement.set_parent(self)
    
    def insert_statement(self, index: int, statement: IStatement) -> None:
        """Insert a statement at a specific position."""
        self.body.insert(index, statement)
        if isinstance(statement, AstNode):
            statement.set_parent(self)
    
    def remove_statement(self, statement: IStatement) -> bool:
        """Remove a statement from the program."""
        if statement in self.body:
            self.body.remove(statement)
            return True
        return False
