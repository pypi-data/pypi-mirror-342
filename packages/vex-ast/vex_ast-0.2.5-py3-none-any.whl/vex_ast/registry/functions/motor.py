from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID
from ...types.primitives import INT, FLOAT, BOOL
from ...types.enums import DIRECTION_TYPE, VELOCITY_UNITS, ROTATION_UNITS, BRAKE_TYPE
from ...types.objects import MOTOR

def register_motor_functions():
    """Register motor-related functions in the registry"""
    
    # Motor.spin() method
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
    
    # Motor.stop() method
    stop_params = [
        VexFunctionParameter("mode", BRAKE_TYPE, "COAST", description="Stopping mode (coast, brake, hold)")
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
    
    # Motor.spin_to_position() method
    spin_to_position_params = [
        VexFunctionParameter("position", FLOAT, description="Position to spin to"),
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to spin at"),
        VexFunctionParameter("units_v", VELOCITY_UNITS, "RPM", description="Velocity units"),
        VexFunctionParameter("wait", BOOL, True, description="Whether to wait for completion")
    ]
    
    spin_to_position_signature = VexFunctionSignature(
        name="spin_to_position",
        return_type=VOID,
        parameters=spin_to_position_params,
        description="Spin the motor to an absolute position",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="spin_to_position",
        cpp_name="spinToPosition",
        object_type=MOTOR,
        method_name="spin_to_position"
    )
    
    registry.register_function(spin_to_position_signature)
    
    # Motor.spin_for() method
    spin_for_params = [
        VexFunctionParameter("direction", DIRECTION_TYPE, description="Direction to spin"),
        VexFunctionParameter("amount", FLOAT, description="Amount to spin"),
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to spin at"),
        VexFunctionParameter("units_v", VELOCITY_UNITS, "RPM", description="Velocity units"),
        VexFunctionParameter("wait", BOOL, True, description="Whether to wait for completion")
    ]
    
    spin_for_signature = VexFunctionSignature(
        name="spin_for",
        return_type=VOID,
        parameters=spin_for_params,
        description="Spin the motor for a relative amount",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="spin_for",
        cpp_name="spinFor",
        object_type=MOTOR,
        method_name="spin_for"
    )
    
    registry.register_function(spin_for_signature)
    
    # Motor.set_velocity() method
    set_velocity_params = [
        VexFunctionParameter("velocity", FLOAT, description="Velocity to set"),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    set_velocity_signature = VexFunctionSignature(
        name="set_velocity",
        return_type=VOID,
        parameters=set_velocity_params,
        description="Set the velocity of the motor",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="set_velocity",
        cpp_name="setVelocity",
        object_type=MOTOR,
        method_name="set_velocity"
    )
    
    registry.register_function(set_velocity_signature)
    
    # Motor.set_stopping() method
    set_stopping_params = [
        VexFunctionParameter("mode", BRAKE_TYPE, description="Stopping mode (coast, brake, hold)")
    ]
    
    set_stopping_signature = VexFunctionSignature(
        name="set_stopping",
        return_type=VOID,
        parameters=set_stopping_params,
        description="Set the stopping mode of the motor",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="set_stopping",
        cpp_name="setStopping",
        object_type=MOTOR,
        method_name="set_stopping"
    )
    
    registry.register_function(set_stopping_signature)
    
    # Add more motor functions as needed...

if __name__ == "__main__":
    register_motor_functions()
