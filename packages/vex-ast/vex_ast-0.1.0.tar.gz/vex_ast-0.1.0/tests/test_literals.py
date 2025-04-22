# tests/test_literals.py
import pytest
from vex_ast.ast.literals import NumberLiteral, StringLiteral, BooleanLiteral, NoneLiteral
from vex_ast.visitors.printer import PrintVisitor
from vex_ast.utils.source_location import SourceLocation

class TestLiterals:
    def test_number_literal(self):
        # Test integer
        nl = NumberLiteral(42)
        assert nl.value == 42
        
        # Test float
        nl = NumberLiteral(3.14)
        assert nl.value == 3.14
        
        # Test with location
        loc = SourceLocation(1, 5)
        nl = NumberLiteral(100, loc)
        assert nl.location == loc
        
    def test_string_literal(self):
        sl = StringLiteral("hello")
        assert sl.value == "hello"
        
        # Test empty string
        sl = StringLiteral("")
        assert sl.value == ""
        
    def test_boolean_literal(self):
        # Test True
        bl = BooleanLiteral(True)
        assert bl.value is True
        
        # Test False
        bl = BooleanLiteral(False)
        assert bl.value is False
        
    def test_none_literal(self):
        nl = NoneLiteral()
        assert nl.value is None
        
    def test_visitor_pattern(self):
        # Test that visitor pattern works correctly
        visitor = PrintVisitor()
        
        nl = NumberLiteral(42)
        sl = StringLiteral("hello")
        bl = BooleanLiteral(True)
        none_l = NoneLiteral()
        
        # Just test that these don't raise exceptions
        visitor.visit(nl)
        visitor.visit(sl)
        visitor.visit(bl)
        visitor.visit(none_l)