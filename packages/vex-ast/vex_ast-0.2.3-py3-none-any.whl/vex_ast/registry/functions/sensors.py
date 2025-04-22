from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID, ANY
from ...types.primitives import INT, FLOAT, BOOL
from ...types.enums import DISTANCE_UNITS, ROTATION_UNITS, VELOCITY_UNITS
from ...types.objects import DISTANCE, ROTATION, INERTIAL, OPTICAL, GPS

def register_sensor_functions():
    """Register sensor-related functions in the registry"""
    
    # Distance sensor functions
    
    # Distance.object_distance() method
    object_distance_params = [
        VexFunctionParameter("units", DISTANCE_UNITS, "MM", description="Distance units")
    ]
    
    object_distance_signature = VexFunctionSignature(
        name="object_distance",
        return_type=FLOAT,
        parameters=object_distance_params,
        description="Get the distance to the detected object",
        category=SimulationCategory.SENSOR_READING,
        python_name="object_distance",
        cpp_name="objectDistance",
        object_type=DISTANCE,
        method_name="object_distance"
    )
    
    registry.register_function(object_distance_signature)
    
    # Distance.is_object_detected() method
    is_object_detected_signature = VexFunctionSignature(
        name="is_object_detected",
        return_type=BOOL,
        parameters=[],
        description="Check if an object is detected",
        category=SimulationCategory.SENSOR_READING,
        python_name="is_object_detected",
        cpp_name="isObjectDetected",
        object_type=DISTANCE,
        method_name="is_object_detected"
    )
    
    registry.register_function(is_object_detected_signature)
    
    # Rotation sensor functions
    
    # Rotation.angle() method
    angle_params = [
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units")
    ]
    
    angle_signature = VexFunctionSignature(
        name="angle",
        return_type=FLOAT,
        parameters=angle_params,
        description="Get the angle of the rotation sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="angle",
        cpp_name="angle",
        object_type=ROTATION,
        method_name="angle"
    )
    
    registry.register_function(angle_signature)
    
    # Rotation.reset_position() method
    reset_position_signature = VexFunctionSignature(
        name="reset_position",
        return_type=VOID,
        parameters=[],
        description="Reset the position of the rotation sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="reset_position",
        cpp_name="resetPosition",
        object_type=ROTATION,
        method_name="reset_position"
    )
    
    registry.register_function(reset_position_signature)
    
    # Rotation.set_position() method
    set_position_params = [
        VexFunctionParameter("value", FLOAT, description="Position value to set"),
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units")
    ]
    
    set_position_signature = VexFunctionSignature(
        name="set_position",
        return_type=VOID,
        parameters=set_position_params,
        description="Set the position of the rotation sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="set_position",
        cpp_name="setPosition",
        object_type=ROTATION,
        method_name="set_position"
    )
    
    registry.register_function(set_position_signature)
    
    # Rotation.velocity() method
    velocity_params = [
        VexFunctionParameter("units", VELOCITY_UNITS, "RPM", description="Velocity units")
    ]
    
    velocity_signature = VexFunctionSignature(
        name="velocity",
        return_type=FLOAT,
        parameters=velocity_params,
        description="Get the velocity of the rotation sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="velocity",
        cpp_name="velocity",
        object_type=ROTATION,
        method_name="velocity"
    )
    
    registry.register_function(velocity_signature)
    
    # Inertial sensor functions
    
    # Inertial.calibrate() method
    calibrate_signature = VexFunctionSignature(
        name="calibrate",
        return_type=VOID,
        parameters=[],
        description="Calibrate the inertial sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="calibrate",
        cpp_name="calibrate",
        object_type=INERTIAL,
        method_name="calibrate"
    )
    
    registry.register_function(calibrate_signature)
    
    # Inertial.is_calibrating() method
    is_calibrating_signature = VexFunctionSignature(
        name="is_calibrating",
        return_type=BOOL,
        parameters=[],
        description="Check if the inertial sensor is calibrating",
        category=SimulationCategory.SENSOR_READING,
        python_name="is_calibrating",
        cpp_name="isCalibrating",
        object_type=INERTIAL,
        method_name="is_calibrating"
    )
    
    registry.register_function(is_calibrating_signature)
    
    # Inertial.heading() method
    heading_params = [
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units")
    ]
    
    heading_signature = VexFunctionSignature(
        name="heading",
        return_type=FLOAT,
        parameters=heading_params,
        description="Get the heading of the inertial sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="heading",
        cpp_name="heading",
        object_type=INERTIAL,
        method_name="heading"
    )
    
    registry.register_function(heading_signature)
    
    # Inertial.rotation() method
    rotation_params = [
        VexFunctionParameter("units", ROTATION_UNITS, "DEGREES", description="Rotation units")
    ]
    
    rotation_signature = VexFunctionSignature(
        name="rotation",
        return_type=FLOAT,
        parameters=rotation_params,
        description="Get the rotation of the inertial sensor",
        category=SimulationCategory.SENSOR_READING,
        python_name="rotation",
        cpp_name="rotation",
        object_type=INERTIAL,
        method_name="rotation"
    )
    
    registry.register_function(rotation_signature)
    
    # Add more sensor functions for other sensor types...

if __name__ == "__main__":
    register_sensor_functions()