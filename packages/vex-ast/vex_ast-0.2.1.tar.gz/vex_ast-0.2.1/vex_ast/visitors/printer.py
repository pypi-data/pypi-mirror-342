"""AST printing visitor implementation."""

import io
from typing import Any, List, Optional

from .base import AstVisitor
from ..ast.interfaces import IAstNode

class PrintVisitor(AstVisitor[str]):
    """Visitor that generates a readable string representation of the AST."""
    
    def __init__(self):
        self._output = io.StringIO()
        self._indent_level = 0
    
    def _indent(self) -> None:
        """Write the current indentation."""
        self._output.write('  ' * self._indent_level)
    
    def _write_node_header(self, node: IAstNode, name: str) -> None:
        """Write a standard node header with location info."""
        self._indent()
        self._output.write(f"{name}")
        if node.location:
            self._output.write(f" (at {node.location})")
        self._output.write(":\n")
    
    def _format_value(self, value: Any) -> str:
        """Format a basic value for display."""
        return repr(value)
    
    def generic_visit(self, node: IAstNode) -> str:
        """Default node visitor that displays type and attributes."""
        node_name = node.__class__.__name__
        self._write_node_header(node, node_name)
        
        # Visit fields if present
        if hasattr(node, '_fields'):
            self._indent_level += 1
            for field_name in node._fields:
                value = getattr(node, field_name, None)
                
                # Skip None values
                if value is None:
                    continue
                
                self._indent()
                self._output.write(f"{field_name} = ")
                
                if isinstance(value, IAstNode):
                    self._output.write("\n")
                    self.visit(value)
                elif isinstance(value, list):
                    if not value:
                        self._output.write("[]\n")
                    else:
                        self._output.write("[\n")
                        self._indent_level += 1
                        for i, item in enumerate(value):
                            self._indent()
                            self._output.write(f"[{i}]: ")
                            if isinstance(item, IAstNode):
                                self._output.write("\n")
                                self.visit(item)
                            else:
                                self._output.write(f"{self._format_value(item)}\n")
                        self._indent_level -= 1
                        self._indent()
                        self._output.write("]\n")
                else:
                    self._output.write(f"{self._format_value(value)}\n")
            self._indent_level -= 1
        
        # At the root level, return the accumulated output
        if self._indent_level == 0:
            return self._output.getvalue()
        return ""
    
    # Simple node visitors for concise output
    def visit_identifier(self, node: Any) -> str:
        self._output.write(f"Identifier(name={node.name!r})")
        if node.location:
            self._output.write(f" (at {node.location})")
        return ""
    
    def visit_numberliteral(self, node: Any) -> str:
        self._output.write(f"NumberLiteral(value={node.value!r})")
        if node.location:
            self._output.write(f" (at {node.location})")
        return ""
    
    def visit_stringliteral(self, node: Any) -> str:
        self._output.write(f"StringLiteral(value={node.value!r})")
        if node.location:
            self._output.write(f" (at {node.location})")
        return ""
    
    def visit_booleanliteral(self, node: Any) -> str:
        self._output.write(f"BooleanLiteral(value={node.value!r})")
        if node.location:
            self._output.write(f" (at {node.location})")
        return ""
    
    def visit_noneliteral(self, node: Any) -> str:
        self._output.write(f"NoneLiteral()")
        if node.location:
            self._output.write(f" (at {node.location})")
        return ""
    
    # Program node is the entry point
    def visit_program(self, node: Any) -> str:
        self._output.write("Program:\n")
        self._indent_level += 1
        for i, stmt in enumerate(node.body):
            self._indent()
            self._output.write(f"[{i}]: \n")
            self._indent_level += 1
            self.visit(stmt)
            self._indent_level -= 1
        self._indent_level -= 1
        return self._output.getvalue()
    
    # Delegate all other methods to generic_visit
    visit_expression = generic_visit
    visit_statement = generic_visit
    visit_variablereference = generic_visit
    visit_binaryoperation = generic_visit
    visit_unaryoperation = generic_visit
    visit_functioncall = generic_visit
    visit_keywordargument = generic_visit
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