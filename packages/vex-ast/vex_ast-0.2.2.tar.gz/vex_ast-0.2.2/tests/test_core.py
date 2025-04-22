# tests/test_core.py
import pytest
from vex_ast.ast.core import Program, Expression, Statement
from vex_ast.ast.statements import ExpressionStatement
from vex_ast.ast.expressions import Identifier
from vex_ast.visitors.base import AstVisitor

# Simple test visitor for testing
class TestVisitor(AstVisitor[str]):
    def generic_visit(self, node):
        return "generic"
    
    def visit_program(self, node):
        return "program"
    
    def visit_expression(self, node):
        return "expression"
    
    def visit_statement(self, node):
        return "statement"
    
    # Implement required methods
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

class TestCoreNodes:
    def test_program_node(self):
        body = [ExpressionStatement(Identifier("x"))]
        program = Program(body)
        
        assert program.body == body
        assert program.get_children() == body
        
        # Test visitor pattern
        visitor = TestVisitor()
        result = program.accept(visitor)
        assert result == "program"
        
    def test_expression_base(self):
        # Create a simple Expression subclass for testing
        class TestExpression(Expression):
            def get_children(self):
                return []
        
        expr = TestExpression()
        
        # Test visitor pattern
        visitor = TestVisitor()
        result = expr.accept(visitor)
        assert result == "expression"
        
    def test_statement_base(self):
        # Create a simple Statement subclass for testing
        class TestStatement(Statement):
            def get_children(self):
                return []
        
        stmt = TestStatement()
        
        # Test visitor pattern
        visitor = TestVisitor()
        result = stmt.accept(visitor)
        assert result == "statement"