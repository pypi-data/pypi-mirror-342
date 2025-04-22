"""Tests for the AST navigator."""

import pytest
from vex_ast import parse_string, create_navigator
from vex_ast.ast.expressions import Identifier, VariableReference, FunctionCall
from vex_ast.ast.statements import Assignment, FunctionDefinition
from vex_ast.ast.literals import NumberLiteral, StringLiteral
from vex_ast.ast.vex_nodes import VexAPICall

class TestAstNavigator:
    """Test the AST navigator functionality."""
    
    def test_basic_navigation(self):
        """Test basic navigation functionality."""
        code = """
        # Define a motor
        motor1 = Motor(PORT1)
        
        # Define a function
        def move_forward(speed):
            motor1.spin(FORWARD, speed, PERCENT)
            wait(1, SECONDS)
            motor1.stop()
            return True
        
        # Call the function
        success = move_forward(50)
        """
        
        # Parse the code
        ast = parse_string(code)
        
        # Create a navigator
        navigator = create_navigator(ast)
        
        # Test finding all identifiers
        identifiers = navigator.find_identifiers()
        assert len(identifiers) > 0
        assert any(ident.name == "motor1" for ident in identifiers)
        assert any(ident.name == "move_forward" for ident in identifiers)
        
        # Test finding all function calls
        function_calls = navigator.find_function_calls()
        assert len(function_calls) > 0
        
        # Test finding VEX API calls
        vex_calls = navigator.find_vex_api_calls()
        assert len(vex_calls) > 0
        
        # Test finding function definitions
        func_defs = navigator.find_function_definitions()
        assert len(func_defs) == 1
        assert func_defs[0].name == "move_forward"
        
        # Test finding assignments
        assignments = navigator.find_assignments()
        assert len(assignments) > 0
        
        # Test finding literals
        literals = navigator.find_literals()
        assert len(literals) > 0
        
        # Test finding a function by name
        move_forward = navigator.get_function_by_name("move_forward")
        assert move_forward is not None
        assert move_forward.name == "move_forward"
        
        # Test finding variable references
        motor_refs = navigator.get_variable_references("motor1")
        assert len(motor_refs) > 0
    
    def test_parent_child_relationships(self):
        """Test parent-child relationship navigation."""
        code = """
        x = 10
        y = 20
        z = x + y
        """
        
        # Parse the code
        ast = parse_string(code)
        
        # Create a navigator
        navigator = create_navigator(ast)
        
        # Find the assignment 'z = x + y'
        assignments = navigator.find_assignments()
        z_assignment = next(a for a in assignments if hasattr(a.target, 'name') and a.target.name == 'z')
        
        # The right side should be a binary operation
        binary_op = z_assignment.value
        
        # Test parent-child relationship
        assert binary_op.get_parent() is z_assignment
        
        # Test finding siblings
        siblings = navigator.find_siblings(z_assignment)
        assert len(siblings) == 2  # The other two assignments
    
    def test_registry_api_integration(self):
        """Test integration with the registry API."""
        code = """
        motor1 = Motor(PORT1)
        motor1.spin(FORWARD, 50, PERCENT)
        """
        
        # Parse the code
        ast = parse_string(code)
        
        # Create a navigator
        navigator = create_navigator(ast)
        
        # Find VEX API calls
        vex_calls = navigator.find_vex_api_calls()
        assert len(vex_calls) > 0
        
        # Test that the signature is resolved correctly
        spin_call = next(call for call in vex_calls if call.get_function_name() and 'spin' in call.get_function_name())
        signature = spin_call.resolve_signature()
        assert signature is not None
        assert signature.name == "spin"
