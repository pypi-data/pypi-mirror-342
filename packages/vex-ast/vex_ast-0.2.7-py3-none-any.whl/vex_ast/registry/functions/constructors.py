"""Register constructors for VEX objects in the registry."""

from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode
from ...types.base import VOID
from ...types.primitives import INT, FLOAT, BOOL, STRING
from ...types.enums import PORT_TYPE
from ...types.objects import MOTOR, BRAIN, CONTROLLER
from ..categories import VexCategory, BehaviorType

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
        category=VexCategory.MOTOR,
        behavior=BehaviorType.CONFIG,
        python_name="Motor",
        cpp_name="motor"
    )
    
    registry.register_function(motor_signature)
    
    # Brain constructor
    brain_params = []  # Brain doesn't take any parameters
    
    brain_signature = VexFunctionSignature(
        name="Brain",
        return_type=BRAIN,
        parameters=brain_params,
        description="Create a new Brain object",
        category=VexCategory.BRAIN,
        behavior=BehaviorType.CONFIG,
        python_name="Brain",
        cpp_name="brain"
    )
    
    registry.register_function(brain_signature)
    
    # Controller constructor
    controller_params = [
        VexFunctionParameter("id", INT, 1, ParameterMode.VALUE, description="The controller ID (primary = 1, partner = 2)")
    ]
    
    controller_signature = VexFunctionSignature(
        name="Controller",
        return_type=CONTROLLER,
        parameters=controller_params,
        description="Create a new Controller object",
        category=VexCategory.CONTROLLER,
        behavior=BehaviorType.CONFIG,
        python_name="Controller",
        cpp_name="controller"
    )
    
    registry.register_function(controller_signature)
    
    # Add other constructors as needed (MotorGroup, Drivetrain, etc.)

if __name__ == "__main__":
    register_constructor_functions()
