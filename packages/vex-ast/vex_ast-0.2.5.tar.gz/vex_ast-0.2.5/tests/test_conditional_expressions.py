"""
Tests for conditional expressions in the AST.
"""

import pytest
from vex_ast import parse_string, serialize_ast_to_dict, deserialize_ast_from_dict
from vex_ast.ast.expressions import ConditionalExpression
from vex_ast.visitors.printer import PrintVisitor

class TestConditionalExpressions:
    """Test cases for conditional expressions."""
    
    def test_parse_conditional_expression(self):
        """Test parsing a conditional expression."""
        # Python's ternary operator: value_if_true if condition else value_if_false
        code = "result = 'positive' if x > 0 else 'negative'"
        ast = parse_string(code)
        
        # Check the AST structure
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "Assignment"
        
        # Check the conditional expression
        value = ast.body[0].value
        assert isinstance(value, ConditionalExpression)
        assert value.condition.__class__.__name__ == "BinaryOperation"
        assert value.true_expr.__class__.__name__ == "StringLiteral"
        assert value.true_expr.value == "positive"
        assert value.false_expr.__class__.__name__ == "StringLiteral"
        assert value.false_expr.value == "negative"
    
    def test_nested_conditional_expressions(self):
        """Test parsing nested conditional expressions."""
        code = """
        # Nested conditional expressions
        result = 'positive' if x > 0 else 'zero' if x == 0 else 'negative'
        """
        ast = parse_string(code)
        
        # Check the AST structure
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "Assignment"
        
        # Check the outer conditional expression
        value = ast.body[0].value
        assert isinstance(value, ConditionalExpression)
        assert value.true_expr.__class__.__name__ == "StringLiteral"
        assert value.true_expr.value == "positive"
        
        # Check the nested conditional expression
        assert isinstance(value.false_expr, ConditionalExpression)
        assert value.false_expr.true_expr.value == "zero"
        assert value.false_expr.false_expr.value == "negative"
    
    def test_conditional_expression_in_function_call(self):
        """Test conditional expressions used in function calls."""
        code = "print('Even' if x % 2 == 0 else 'Odd')"
        # Explicitly pass a test filename to ensure 'print' is treated as a regular function call
        ast = parse_string(code, filename="test_conditional_expressions.py")
        
        # Check the AST structure
        assert len(ast.body) == 1
        assert ast.body[0].__class__.__name__ == "ExpressionStatement"
        
        # Check the function call
        func_call = ast.body[0].expression
        assert func_call.__class__.__name__ == "FunctionCall"
        
        # Check the conditional expression argument
        assert len(func_call.args) == 1
        arg = func_call.args[0]
        assert isinstance(arg, ConditionalExpression)
        assert arg.true_expr.value == "Even"
        assert arg.false_expr.value == "Odd"
    
    def test_conditional_expression_serialization(self):
        """Test serialization and deserialization of conditional expressions."""
        code = "result = value1 if condition else value2"
        original_ast = parse_string(code)
        
        # Serialize to dictionary
        serialized = serialize_ast_to_dict(original_ast)
        
        # Check serialized structure
        assert serialized["type"] == "Program"
        assert len(serialized["body"]) == 1
        assert serialized["body"][0]["type"] == "Assignment"
        
        # Check the conditional expression
        cond_expr = serialized["body"][0]["value"]
        assert cond_expr["type"] == "ConditionalExpression"
        assert "condition" in cond_expr
        assert "true_expr" in cond_expr
        assert "false_expr" in cond_expr
        
        # Deserialize back to AST
        deserialized_ast = deserialize_ast_from_dict(serialized)
        
        # Check the deserialized AST
        assert len(deserialized_ast.body) == 1
        assert deserialized_ast.body[0].__class__.__name__ == "Assignment"
        
        # Check the conditional expression
        value = deserialized_ast.body[0].value
        assert isinstance(value, ConditionalExpression)
        assert value.condition.__class__.__name__ == "VariableReference"
        assert value.true_expr.__class__.__name__ == "VariableReference"
        assert value.false_expr.__class__.__name__ == "VariableReference"
    
    def test_conditional_expression_printing(self):
        """Test printing conditional expressions."""
        code = "result = 'yes' if condition else 'no'"
        ast = parse_string(code)
        
        # Use the PrintVisitor to convert the AST back to code
        printer = PrintVisitor()
        printed_code = printer.visit(ast)
        
        # The printed code should contain the conditional expression components
        assert "ConditionalExpression" in printed_code
        assert "condition" in printed_code
        assert "true_expr" in printed_code
        assert "false_expr" in printed_code
        assert "'yes'" in printed_code
        assert "'no'" in printed_code
        
        # The printed code should also contain the formatted expression with if/else keywords
        assert "formatted = " in printed_code
        assert "if" in printed_code
        assert "else" in printed_code
