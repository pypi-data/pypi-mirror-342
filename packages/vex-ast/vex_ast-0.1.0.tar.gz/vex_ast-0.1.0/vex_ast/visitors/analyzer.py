"""Analysis visitors for AST."""

from typing import Any, Dict, List, Optional, Set

from .base import AstVisitor
from ..ast.interfaces import IAstNode

class NodeCounter(AstVisitor[int]):
    """Visitor that counts nodes in the AST."""
    
    def __init__(self):
        self.count = 0
        self.counts_by_type: Dict[str, int] = {}
    
    def generic_visit(self, node: IAstNode) -> int:
        """Count this node and visit its children."""
        self.count += 1
        
        # Count by node type
        node_type = node.__class__.__name__
        self.counts_by_type[node_type] = self.counts_by_type.get(node_type, 0) + 1
        
        # Visit all children
        for child in node.get_children():
            self.visit(child)
        
        return self.count
    
    # Implement all the required visit methods by delegating to generic_visit
    visit_program = generic_visit
    visit_expression = generic_visit
    visit_statement = generic_visit
    visit_identifier = generic_visit
    visit_variablereference = generic_visit
    visit_binaryoperation = generic_visit
    visit_unaryoperation = generic_visit
    visit_functioncall = generic_visit
    visit_keywordargument = generic_visit
    visit_numberliteral = generic_visit
    visit_stringliteral = generic_visit
    visit_booleanliteral = generic_visit
    visit_noneliteral = generic_visit
    visit_expressionstatement = generic_visit
    visit_assignment = generic_visit
    visit_ifstatement = generic_visit
    visit_whileloop = generic_visit
    visit_forloop = generic_visit
    visit_functiondefinition = generic_visit
    visit_argument = generic_visit
    visit_returnstatement = generic_visit
    visit_breakstatement = generic_visit
    visit_continuestatement = generic_visit
    visit_vexapicall = generic_visit
    visit_motorcontrol = generic_visit
    visit_sensorreading = generic_visit
    visit_timingcontrol = generic_visit
    visit_displayoutput = generic_visit

class VariableCollector(AstVisitor[Set[str]]):
    """Visitor that collects variable names used in the AST."""
    
    def __init__(self):
        self.variables: Set[str] = set()
    
    def generic_visit(self, node: IAstNode) -> Set[str]:
        """Collect variables from children."""
        for child in node.get_children():
            self.visit(child)
        return self.variables
    
    def visit_variablereference(self, node: Any) -> Set[str]:
        """Collect a variable reference."""
        self.variables.add(node.name)
        return self.generic_visit(node)
    
    # Delegate all other methods to generic_visit
    visit_program = generic_visit
    visit_expression = generic_visit
    visit_statement = generic_visit
    visit_identifier = generic_visit
    visit_binaryoperation = generic_visit
    visit_unaryoperation = generic_visit
    visit_functioncall = generic_visit
    visit_keywordargument = generic_visit
    visit_numberliteral = generic_visit
    visit_stringliteral = generic_visit
    visit_booleanliteral = generic_visit
    visit_noneliteral = generic_visit
    visit_expressionstatement = generic_visit
    visit_assignment = generic_visit
    visit_ifstatement = generic_visit
    visit_whileloop = generic_visit
    visit_forloop = generic_visit
    visit_functiondefinition = generic_visit
    visit_argument = generic_visit
    visit_returnstatement = generic_visit
    visit_breakstatement = generic_visit
    visit_continuestatement = generic_visit
    visit_vexapicall = generic_visit
    visit_motorcontrol = generic_visit
    visit_sensorreading = generic_visit
    visit_timingcontrol = generic_visit
    visit_displayoutput = generic_visit