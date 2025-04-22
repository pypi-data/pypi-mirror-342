# tests/conftest.py
import os
import sys
import pytest

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initialize registry for tests
@pytest.fixture(scope="session", autouse=True)
def initialize_registry():
    """Initialize the registry with test functions."""
    from vex_ast.registry.functions.initialize import initialize_registry
    from vex_ast.registry.api import registry_api
    
    # Force registry initialization
    initialize_registry()
    
    # Add a test function if registry is empty
    if len(registry_api.get_all_functions()) == 0:
        from vex_ast.registry.registry import registry
        from vex_ast.registry.signature import VexFunctionSignature, VexFunctionParameter, SimulationCategory
        from vex_ast.types.base import VOID
        from vex_ast.types.primitives import INT, FLOAT, BOOL
        from vex_ast.types.enums import DIRECTION_TYPE, VELOCITY_UNITS
        from vex_ast.types.objects import MOTOR
        
        # Add a test motor.spin function
        spin_params = [
            VexFunctionParameter("direction", DIRECTION_TYPE, description="Direction to spin the motor"),
            VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to spin at"),
            VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
        ]
        
        spin_signature = VexFunctionSignature(
            name="spin",
            return_type=VOID,
            parameters=spin_params,
            description="Spin the motor in the specified direction",
            category=SimulationCategory.MOTOR_CONTROL,
            python_name="spin",
            cpp_name="spin",
            object_type=MOTOR,
            method_name="spin"
        )
        
        registry.register_function(spin_signature)
        
        # Add a test motor.stop function
        stop_params = [
            VexFunctionParameter("mode", DIRECTION_TYPE, "COAST", description="Stopping mode")
        ]
        
        stop_signature = VexFunctionSignature(
            name="stop",
            return_type=VOID,
            parameters=stop_params,
            description="Stop the motor",
            category=SimulationCategory.MOTOR_CONTROL,
            python_name="stop",
            cpp_name="stop",
            object_type=MOTOR,
            method_name="stop"
        )
        
        registry.register_function(stop_signature)
        
        print(f"Added test functions to registry. Total functions: {len(registry_api.get_all_functions())}")
