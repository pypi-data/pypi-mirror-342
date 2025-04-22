# tests/test_parser.py
import pytest
from vex_ast import parse_string
from vex_ast.utils.errors import ErrorHandler, VexSyntaxError
from vex_ast.visitors.printer import PrintVisitor
from vex_ast.visitors.analyzer import NodeCounter, VariableCollector

class TestParser:
    def test_parse_basic_expression(self):
        code = "x = 42"
        ast = parse_string(code)
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "Assignment"
        
    def test_parse_function_definition(self):
        code = """
        def test(x, y=10):
            return x + y
        """
        ast = parse_string(code)
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "FunctionDefinition"
        
    def test_parse_if_statement(self):
        code = """
        if condition:
            x = 1
        elif other_condition:
            x = 2
        else:
            x = 3
        """
        ast = parse_string(code)
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "IfStatement"
        
    def test_parse_loops(self):
        code = """
        # While loop
        while condition:
            x += 1
            
        # For loop
        for i in range(10):
            print(i)
        """
        ast = parse_string(code)
        assert len(ast.body) == 2
        assert ast.body[0].__class__.__name__ == "WhileLoop"
        assert ast.body[1].__class__.__name__ == "ForLoop"
        
    def test_syntax_error(self):
        code = "if x =="  # Incomplete if statement
        with pytest.raises(VexSyntaxError):
            parse_string(code)
            
    def test_with_error_handler(self):
        code = "if x =="  # Incomplete if statement
        error_handler = ErrorHandler(raise_on_error=False)
        
        # Should not raise an exception when raise_on_error=False
        ast = parse_string(code, error_handler=error_handler)
        
        # But should collect errors
        assert error_handler.has_errors()
        errors = error_handler.get_errors()
        assert len(errors) >= 1
