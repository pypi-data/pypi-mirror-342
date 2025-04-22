# tests/test_visitors.py
import pytest
from vex_ast import parse_string
from vex_ast.visitors.printer import PrintVisitor
from vex_ast.visitors.analyzer import NodeCounter, VariableCollector
from vex_ast.ast.core import Program
from vex_ast.ast.literals import NumberLiteral, StringLiteral

class TestVisitors:
    def test_print_visitor(self):
        # Test with simple AST
        ast = parse_string("x = 42")
        visitor = PrintVisitor()
        result = visitor.visit(ast)
        
        # Basic check that it returns a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
    def test_node_counter(self):
        code = """
        def test(x):
            y = x + 1
            return y
            
        result = test(5)
        """
        ast = parse_string(code)
        counter = NodeCounter()
        count = counter.visit(ast)
        
        # We should have more than 5 nodes
        assert count > 5
        
        # Check specific node types
        counts = counter.counts_by_type
        assert "Program" in counts
        assert counts["Program"] == 1
        assert "FunctionDefinition" in counts
        assert "Assignment" in counts
        
    def test_variable_collector(self):
        code = """
        x = 10
        y = 20
        z = x + y
        """
        ast = parse_string(code)
        collector = VariableCollector()
        variables = collector.visit(ast)
        
        assert "x" in variables
        assert "y" in variables
        # z is only a target, not a reference
        assert "z" not in variables