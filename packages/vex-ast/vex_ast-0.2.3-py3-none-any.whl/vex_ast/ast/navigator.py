"""AST navigation utilities.

This module provides utilities for navigating the AST structure,
hiding implementation details and providing a more stable interface.
"""

from typing import Dict, List, Optional, Set, Iterator, TypeVar, Generic, Type, cast, Any, Union

from .interfaces import IAstNode, IExpression, IStatement, ILiteral, IIdentifier, IFunctionCall
from .core import Program
from .expressions import (
    Identifier, VariableReference, AttributeAccess, 
    BinaryOperation, UnaryOperation, FunctionCall
)
from .statements import (
    ExpressionStatement, Assignment, FunctionDefinition,
    IfStatement, WhileLoop, ForLoop, ReturnStatement
)
from .literals import NumberLiteral, StringLiteral, BooleanLiteral
from .vex_nodes import VexAPICall

T = TypeVar('T', bound=IAstNode)

class AstNavigator:
    """Navigator for traversing and querying the AST."""
    
    def __init__(self, root: IAstNode):
        """Initialize with a root node."""
        self.root = root
    
    def find_all(self, node_type: Type[T]) -> List[T]:
        """Find all nodes of a specific type in the AST.
        
        Args:
            node_type: The type of node to find
            
        Returns:
            List of nodes matching the type
        """
        result: List[T] = []
        self._find_all_recursive(self.root, node_type, result)
        return result
    
    def _find_all_recursive(self, node: IAstNode, node_type: Type[T], result: List[T]) -> None:
        """Recursively find all nodes of a specific type."""
        if isinstance(node, node_type):
            result.append(cast(T, node))
        
        for child in node.get_children():
            self._find_all_recursive(child, node_type, result)
    
    def find_first(self, node_type: Type[T]) -> Optional[T]:
        """Find the first node of a specific type in the AST.
        
        Args:
            node_type: The type of node to find
            
        Returns:
            The first node matching the type, or None if not found
        """
        return next(self.find_iter(node_type), None)
    
    def find_iter(self, node_type: Type[T]) -> Iterator[T]:
        """Find all nodes of a specific type as an iterator.
        
        Args:
            node_type: The type of node to find
            
        Returns:
            Iterator of nodes matching the type
        """
        for node in self._traverse_iter(self.root):
            if isinstance(node, node_type):
                yield cast(T, node)
    
    def _traverse_iter(self, node: IAstNode) -> Iterator[IAstNode]:
        """Traverse the AST in pre-order."""
        yield node
        for child in node.get_children():
            yield from self._traverse_iter(child)
    
    def find_parent(self, node: IAstNode) -> Optional[IAstNode]:
        """Find the parent of a node.
        
        Args:
            node: The node to find the parent of
            
        Returns:
            The parent node, or None if not found or if the node is the root
        """
        return node.get_parent()
    
    def find_ancestors(self, node: IAstNode) -> List[IAstNode]:
        """Find all ancestors of a node.
        
        Args:
            node: The node to find ancestors of
            
        Returns:
            List of ancestor nodes, from immediate parent to root
        """
        result: List[IAstNode] = []
        current = node.get_parent()
        while current:
            result.append(current)
            current = current.get_parent()
        return result
    
    def find_siblings(self, node: IAstNode) -> List[IAstNode]:
        """Find all siblings of a node.
        
        Args:
            node: The node to find siblings of
            
        Returns:
            List of sibling nodes, excluding the node itself
        """
        parent = node.get_parent()
        if not parent:
            return []
        
        return [child for child in parent.get_children() if child is not node]
    
    # Specific node type finders
    
    def find_identifiers(self) -> List[IIdentifier]:
        """Find all identifiers in the AST."""
        return self.find_all(Identifier)
    
    def find_function_calls(self) -> List[IFunctionCall]:
        """Find all function calls in the AST."""
        return self.find_all(FunctionCall)
    
    def find_vex_api_calls(self) -> List[VexAPICall]:
        """Find all VEX API calls in the AST."""
        return self.find_all(VexAPICall)
    
    def find_assignments(self) -> List[Assignment]:
        """Find all assignments in the AST."""
        return self.find_all(Assignment)
    
    def find_function_definitions(self) -> List[FunctionDefinition]:
        """Find all function definitions in the AST."""
        return self.find_all(FunctionDefinition)
    
    def find_if_statements(self) -> List[IfStatement]:
        """Find all if statements in the AST."""
        return self.find_all(IfStatement)
    
    def find_loops(self) -> List[Union[WhileLoop, ForLoop]]:
        """Find all loops in the AST."""
        while_loops = self.find_all(WhileLoop)
        for_loops = self.find_all(ForLoop)
        return cast(List[Union[WhileLoop, ForLoop]], while_loops + for_loops)
    
    def find_return_statements(self) -> List[ReturnStatement]:
        """Find all return statements in the AST."""
        return self.find_all(ReturnStatement)
    
    def find_literals(self) -> List[ILiteral]:
        """Find all literals in the AST."""
        return cast(List[ILiteral], 
                   self.find_all(NumberLiteral) + 
                   self.find_all(StringLiteral) + 
                   self.find_all(BooleanLiteral))
    
    # Program-specific methods
    
    def get_statements(self) -> List[IStatement]:
        """Get all top-level statements in the program."""
        if isinstance(self.root, Program):
            return self.root.get_statements()
        return []
    
    def get_function_by_name(self, name: str) -> Optional[FunctionDefinition]:
        """Find a function definition by name.
        
        Args:
            name: The function name
            
        Returns:
            The function definition, or None if not found
        """
        for func in self.find_function_definitions():
            if func.get_name() == name:
                return func
        return None
    
    def get_variable_references(self, name: str) -> List[VariableReference]:
        """Find all references to a variable.
        
        Args:
            name: The variable name
            
        Returns:
            List of variable references
        """
        return [ref for ref in self.find_all(VariableReference) if ref.name == name]
    
    def get_attribute_accesses(self, object_name: str) -> List[AttributeAccess]:
        """Find all attribute accesses on an object.
        
        Args:
            object_name: The object name
            
        Returns:
            List of attribute accesses
        """
        result = []
        for access in self.find_all(AttributeAccess):
            if hasattr(access.object, 'name') and getattr(access.object, 'name') == object_name:
                result.append(access)
        return result


def create_navigator(ast_node: IAstNode) -> AstNavigator:
    """Create a new AST navigator for the given AST node.
    
    Args:
        ast_node: The AST node to navigate
        
    Returns:
        A new AstNavigator instance
    """
    return AstNavigator(ast_node)
