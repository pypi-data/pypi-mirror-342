"""Base visitor classes for AST traversal."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar, cast, Type

from ..ast.interfaces import IAstNode, T_VisitorResult

class AstVisitor(Generic[T_VisitorResult], ABC):
    """Base class for AST visitors using the Visitor pattern."""
    
    def visit(self, node: IAstNode) -> T_VisitorResult:
        """Visit a node by dispatching to its accept method."""
        return node.accept(self)
    
    def visit_children(self, node: IAstNode) -> List[T_VisitorResult]:
        """Visit all children of a node and return results."""
        return [self.visit(child) for child in node.get_children()]
    
    @abstractmethod
    def generic_visit(self, node: IAstNode) -> T_VisitorResult:
        """Default visitor method for nodes without a specific method."""
        pass
    
    # Required visit methods for core node types
    def visit_program(self, node: Any) -> T_VisitorResult: 
        return self.generic_visit(node)
    
    def visit_expression(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_statement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    # Visit methods for expressions
    def visit_identifier(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_variablereference(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_attributeaccess(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_binaryoperation(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_unaryoperation(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_functioncall(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_keywordargument(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    # Visit methods for literals
    def visit_numberliteral(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_stringliteral(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_booleanliteral(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_noneliteral(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    # Visit methods for statements
    def visit_expressionstatement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_assignment(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_ifstatement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_whileloop(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_forloop(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_functiondefinition(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_argument(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_returnstatement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_breakstatement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_continuestatement(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    # Visit methods for VEX-specific nodes
    def visit_vexapicall(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_motorcontrol(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_sensorreading(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_timingcontrol(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)
    
    def visit_displayoutput(self, node: Any) -> T_VisitorResult:
        return self.generic_visit(node)


class TypedVisitorMixin:
    """Mixin to provide type-specific dispatch methods."""
    
    @staticmethod
    def node_type_to_method_name(node_type: Type) -> str:
        """Convert a node type to a visitor method name."""
        return f"visit_{node_type.__name__.lower()}"
    
    def dispatch_by_type(self, node: IAstNode) -> Any:
        """Dispatch to the appropriate visit method based on the node's type."""
        method_name = self.node_type_to_method_name(type(node))
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        return self.generic_visit(node)