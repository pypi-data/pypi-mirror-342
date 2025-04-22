from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID
from ...types.primitives import INT, FLOAT, BOOL
from ...types.enums import DIRECTION_TYPE, TURN_TYPE, VELOCITY_UNITS, ROTATION_UNITS, DISTANCE_UNITS, BRAKE_TYPE
from ...types.objects import DRIVETRAIN

def register_drivetrain_functions():
    """Register drivetrain-related functions in the registry"""
    
    # Drivetrain.drive() method
    drive_params = [
        VexFunctionParameter("direction", DIRECTION_TYPE, description="Direction to drive"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to drive at"),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    drive_signature = VexFunctionSignature(
        name="drive",
        return_type=VOID,
        parameters=drive_params,
        description="Drive the drivetrain in the specified direction",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="drive",
        cpp_name="drive",
        object_type=DRIVETRAIN,
        method_name="drive"
    )
    
    registry.register_function(drive_signature)
    
    # Drivetrain.drive_for() method
    drive_for_params = [
        VexFunctionParameter("direction", DIRECTION_TYPE, description="Direction to drive"),
        VexFunctionParameter("distance", FLOAT, description="Distance to drive"),
        VexFunctionParameter("units", DISTANCE_UNITS, "INCHES", description="Distance units"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to drive at"),
        VexFunctionParameter("units_v", VELOCITY_UNITS, "RPM", description="Velocity units"),
        VexFunctionParameter("wait", BOOL, True, description="Whether to wait for completion")
    ]
    
    drive_for_signature = VexFunctionSignature(
        name="drive_for",
        return_type=VOID,
        parameters=drive_for_params,
        description="Drive the drivetrain for a specific distance",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="drive_for",
        cpp_name="driveFor",
        object_type=DRIVETRAIN,
        method_name="drive_for"
    )
    
    registry.register_function(drive_for_signature)
    
    # Drivetrain.turn() method
    turn_params = [
        VexFunctionParameter("direction", TURN_TYPE, description="Direction to turn"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to turn at"),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    turn_signature = VexFunctionSignature(
        name="turn",
        return_type=VOID,
        parameters=turn_params,
        description="Turn the drivetrain in the specified direction",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="turn",
        cpp_name="turn",
        object_type=DRIVETRAIN,
        method_name="turn"
    )
    
    registry.register_function(turn_signature)
    
    # Drivetrain.turn_for() method
    turn_for_params = [
        VexFunctionParameter("direction", TURN_TYPE, description="Direction to turn"),
        VexFunctionParameter("angle", FLOAT, description="Angle to turn"),
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units"),
        VexFunctionParameter("velocity", FLOAT, 50.0, description="Velocity to turn at"),
        VexFunctionParameter("units_v", VELOCITY_UNITS, "RPM", description="Velocity units"),
        VexFunctionParameter("wait", BOOL, True, description="Whether to wait for completion")
    ]
    
    turn_for_signature = VexFunctionSignature(
        name="turn_for",
        return_type=VOID,
        parameters=turn_for_params,
        description="Turn the drivetrain for a specific angle",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="turn_for",
        cpp_name="turnFor",
        object_type=DRIVETRAIN,
        method_name="turn_for"
    )
    
    registry.register_function(turn_for_signature)
    
    # Drivetrain.stop() method
    stop_params = [
        VexFunctionParameter("mode", BRAKE_TYPE, "COAST", description="Stopping mode (coast, brake, hold)")
    ]
    
    stop_signature = VexFunctionSignature(
        name="stop",
        return_type=VOID,
        parameters=stop_params,
        description="Stop the drivetrain",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="stop",
        cpp_name="stop",
        object_type=DRIVETRAIN,
        method_name="stop"
    )
    
    registry.register_function(stop_signature)
    
    # Drivetrain.set_drive_velocity() method
    set_drive_velocity_params = [
        VexFunctionParameter("velocity", FLOAT, description="Velocity to set"),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    set_drive_velocity_signature = VexFunctionSignature(
        name="set_drive_velocity",
        return_type=VOID,
        parameters=set_drive_velocity_params,
        description="Set the drive velocity of the drivetrain",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="set_drive_velocity",
        cpp_name="setDriveVelocity",
        object_type=DRIVETRAIN,
        method_name="set_drive_velocity"
    )
    
    registry.register_function(set_drive_velocity_signature)
    
    # Drivetrain.set_turn_velocity() method
    set_turn_velocity_params = [
        VexFunctionParameter("velocity", FLOAT, description="Velocity to set"),
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    set_turn_velocity_signature = VexFunctionSignature(
        name="set_turn_velocity",
        return_type=VOID,
        parameters=set_turn_velocity_params,
        description="Set the turn velocity of the drivetrain",
        category=SimulationCategory.MOTOR_CONTROL,
        python_name="set_turn_velocity",
        cpp_name="setTurnVelocity",
        object_type=DRIVETRAIN,
        method_name="set_turn_velocity"
    )
    
    registry.register_function(set_turn_velocity_signature)
    
    # Add more drivetrain functions as needed...

if __name__ == "__main__":
    register_drivetrain_functions()
