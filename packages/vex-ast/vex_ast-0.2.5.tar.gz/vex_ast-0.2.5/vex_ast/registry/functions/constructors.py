"""Register constructors for VEX objects in the registry."""

from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID
from ...types.primitives import INT, FLOAT, BOOL, STRING
from ...types.enums import PORT_TYPE
from ...types.objects import MOTOR

def register_constructor_functions():
    """Register constructor functions in the registry"""
    
    # Motor constructor
    motor_params = [
        VexFunctionParameter("port", PORT_TYPE, description="The port the motor is connected to"),
        VexFunctionParameter("gear_ratio", FLOAT, None, ParameterMode.VALUE, description="The gear ratio of the motor"),
        VexFunctionParameter("reverse", BOOL, False, ParameterMode.VALUE, description="Whether to reverse the motor direction")
    ]
    
    motor_signature = VexFunctionSignature(
        name="Motor",
        return_type=MOTOR,
        parameters=motor_params,
        description="Create a new Motor object",
        category=SimulationCategory.CONFIGURATION,
        python_name="Motor",
        cpp_name="motor"
    )
    
    registry.register_function(motor_signature)
    
    # Add other constructors as needed (MotorGroup, Drivetrain, etc.)

if __name__ == "__main__":
    register_constructor_functions()
