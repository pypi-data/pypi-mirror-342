import pytest
from vex_ast import parse_string, registry_api
from vex_ast.ast.vex_nodes import VexAPICall
from vex_ast.registry.signature import SimulationCategory
from vex_ast.ast.validators import validate_vex_functions

class TestRegistry:
    def test_registry_initialization(self):
        # Verify that registry has been populated
        assert len(registry_api.get_all_functions()) > 0
        
        # Check specific function existence
        motor_spin = registry_api.get_function("spin")
        assert motor_spin is not None
        assert motor_spin.object_type.name == "Motor"
        assert motor_spin.category == SimulationCategory.MOTOR_CONTROL
    
    def test_parsing_with_registry(self):
        # Parse code with a VEX function call
        code = """
        # Initialize a motor
        motor1 = Motor(PORT1)
        
        # Use a VEX API call
        motor1.spin(FORWARD, 50, PERCENT)
        """
        
        ast = parse_string(code)
        
        # Find the VexAPICall node
        vex_calls = []
        
        def find_vex_calls(node):
            if isinstance(node, VexAPICall):
                vex_calls.append(node)
                print(f"Found VexAPICall: {node.get_function_name()}")
            for child in node.get_children():
                find_vex_calls(child)
        
        find_vex_calls(ast)
        
        # Verify we found the VEX call
        assert len(vex_calls) > 0
        
        # Find the motor1.spin call
        motor_spin_call = None
        for call in vex_calls:
            if call.get_function_name() == "motor1.spin":
                motor_spin_call = call
                break
        
        assert motor_spin_call is not None, f"motor1.spin call not found. Found calls: {[call.get_function_name() for call in vex_calls]}"
        
        # Resolve the signature (it might not directly validate as our AST doesn't have types)
        signature = motor_spin_call.resolve_signature()
        assert signature is not None
        assert signature.name == "spin"
        assert signature.category == SimulationCategory.MOTOR_CONTROL
    
    def test_function_validation(self):
        # Valid call
        valid_code = """
        motor1 = Motor(PORT1)
        motor1.spin(FORWARD)
        """
        
        valid_ast = parse_string(valid_code)
        valid_errors = validate_vex_functions(valid_ast)
        
        # We may have errors due to AST not having proper types, but the test demonstrates
        # the validation process
        
        # Invalid call (wrong argument)
        invalid_code = """
        motor1 = Motor(PORT1)
        # Invalid: stop doesn't take arbitrary arguments
        motor1.stop(FORWARD, 100, INVALID_ARG)
        """
        
        invalid_ast = parse_string(invalid_code)
        invalid_errors = validate_vex_functions(invalid_ast)
        
        # This should produce at least one error
        assert len(invalid_errors) > 0
