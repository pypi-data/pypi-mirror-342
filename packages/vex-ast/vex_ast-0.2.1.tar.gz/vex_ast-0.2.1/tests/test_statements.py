# tests/test_statements.py
import pytest
from vex_ast.ast.statements import (
    ExpressionStatement, Assignment, IfStatement,
    WhileLoop, ForLoop, FunctionDefinition, ReturnStatement,
    BreakStatement, ContinueStatement, Argument
)
from vex_ast.ast.expressions import Identifier, VariableReference
from vex_ast.ast.literals import NumberLiteral, BooleanLiteral

class TestStatements:
    def test_expression_statement(self):
        expr = Identifier("x")
        stmt = ExpressionStatement(expr)
        assert stmt.expression == expr
        assert stmt.get_children() == [expr]
        
    def test_assignment(self):
        target = Identifier("x")
        value = NumberLiteral(42)
        assign = Assignment(target, value)
        
        assert assign.target == target
        assert assign.value == value
        assert assign.get_children() == [target, value]
        
    def test_if_statement(self):
        test = BooleanLiteral(True)
        body = [ExpressionStatement(Identifier("x"))]
        
        # If without else
        if_stmt = IfStatement(test, body)
        assert if_stmt.test == test
        assert if_stmt.body == body
        assert if_stmt.orelse is None
        
        # If with else
        else_body = [ExpressionStatement(Identifier("y"))]
        if_with_else = IfStatement(test, body, else_body)
        assert if_with_else.orelse == else_body
        
        # If with elif (nested if)
        elif_stmt = IfStatement(BooleanLiteral(False), else_body)
        if_with_elif = IfStatement(test, body, elif_stmt)
        assert if_with_elif.orelse == elif_stmt
        
    def test_while_loop(self):
        test = BooleanLiteral(True)
        body = [ExpressionStatement(Identifier("x"))]
        
        while_loop = WhileLoop(test, body)
        assert while_loop.test == test
        assert while_loop.body == body
        assert while_loop.get_children() == [test] + body
        
    def test_for_loop(self):
        target = Identifier("i")
        iterable = Identifier("items")
        body = [ExpressionStatement(Identifier("x"))]
        
        for_loop = ForLoop(target, iterable, body)
        assert for_loop.target == target
        assert for_loop.iterable == iterable
        assert for_loop.body == body
        assert for_loop.get_children() == [target, iterable] + body
        
    def test_function_definition(self):
        name = "test_func"
        args = [Argument("x"), Argument("y", None, NumberLiteral(0))]
        body = [ReturnStatement(Identifier("x"))]
        
        func_def = FunctionDefinition(name, args, body)
        assert func_def.name == name
        assert func_def.args == args
        assert func_def.body == body
        assert func_def.return_annotation is None
        
        # Check children
        children = func_def.get_children()
        for arg in args:
            assert arg in children
        for stmt in body:
            assert stmt in children
            
    def test_return_statement(self):
        # Return with value
        value = NumberLiteral(42)
        ret = ReturnStatement(value)
        assert ret.value == value
        assert ret.get_children() == [value]
        
        # Return without value
        empty_ret = ReturnStatement()
        assert empty_ret.value is None
        assert empty_ret.get_children() == []
        
    def test_break_statement(self):
        br = BreakStatement()
        assert br.get_children() == []
        
    def test_continue_statement(self):
        cont = ContinueStatement()
        assert cont.get_children() == []