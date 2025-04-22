"""
Types package for VEX AST.

This package provides type definitions and type checking functionality for VEX AST.
"""

from .base import (
    VexType,
    VoidType,
    AnyType,
    TypeRegistry,
    VOID,
    ANY,
    type_registry
)

from .primitives import (
    PrimitiveType,
    IntegerType,
    FloatType,
    BooleanType,
    StringType,
    INT,
    FLOAT,
    BOOL,
    STRING
)

from .objects import (
    ObjectType,
    MOTOR,
    MOTOR_GROUP,
    DRIVETRAIN,
    BRAIN,
    CONTROLLER,
    INERTIAL,
    DISTANCE,
    ROTATION,
    OPTICAL,
    GPS,
    ELECTROMAGNETIC,
    BRAIN_BATTERY,
    BRAIN_SCREEN,
    BRAIN_LCD,
    COMPETITION,
    TIMER,
    BUMPER,
    LIMIT_SWITCH,
    ENCODER,
    SONAR,
    GYRO,
    PNEUMATIC,
    VISION
)

from .enums import (
    EnumType,
    DIRECTION_TYPE,
    TURN_TYPE,
    BRAKE_TYPE,
    VELOCITY_UNITS,
    ROTATION_UNITS,
    TIME_UNITS,
    DISTANCE_UNITS,
    CURRENT_UNITS,
    TORQUE_UNITS,
    TEMPERATURE_UNITS,
    ANALOG_UNITS
)

from .type_checker import (
    TypeChecker,
    type_checker as check_type_compatibility
)

__all__ = [
    # Base types
    "VexType",
    "VoidType",
    "AnyType",
    "TypeRegistry",
    "VOID",
    "ANY",
    "type_registry",
    
    # Primitive types
    "PrimitiveType",
    "IntegerType",
    "FloatType",
    "BooleanType",
    "StringType",
    "INT",
    "FLOAT",
    "BOOL",
    "STRING",
    
    # Object types
    "ObjectType",
    "MOTOR",
    "MOTOR_GROUP",
    "DRIVETRAIN",
    "BRAIN",
    "CONTROLLER",
    "INERTIAL",
    "DISTANCE",
    "ROTATION",
    "OPTICAL",
    "GPS",
    "ELECTROMAGNETIC",
    "BRAIN_BATTERY",
    "BRAIN_SCREEN",
    "BRAIN_LCD",
    "COMPETITION",
    "TIMER",
    "BUMPER",
    "LIMIT_SWITCH",
    "ENCODER",
    "SONAR",
    "GYRO",
    "PNEUMATIC",
    "VISION",
    
    # Enum types
    "EnumType",
    "DIRECTION_TYPE",
    "TURN_TYPE",
    "BRAKE_TYPE",
    "VELOCITY_UNITS",
    "ROTATION_UNITS",
    "TIME_UNITS",
    "DISTANCE_UNITS",
    "CURRENT_UNITS",
    "TORQUE_UNITS",
    "TEMPERATURE_UNITS",
    "ANALOG_UNITS",
    
    # Type checking
    "TypeChecker",
    "check_type_compatibility"
]
