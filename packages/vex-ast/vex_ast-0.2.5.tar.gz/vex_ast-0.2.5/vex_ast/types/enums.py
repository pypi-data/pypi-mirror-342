from typing import Dict, List, Any, Optional, Set
from .base import VexType, type_registry
from .primitives import StringType, IntegerType, INT

class EnumType(VexType):
    """Represents a VEX enum type"""
    
    def __init__(self, name: str, values: Dict[str, Any] = None):
        self._name = name
        self._values = values or {}
        type_registry.register_type(self)
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def values(self) -> Dict[str, Any]:
        return self._values.copy()
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Enums are compatible with themselves or with integers"""
        return isinstance(other, EnumType) and self.name == other.name or isinstance(other, IntegerType)
    
    def __str__(self) -> str:
        return f"enum {self._name}"
    
    def add_value(self, name: str, value: Any) -> None:
        """Add a value to the enum"""
        self._values[name] = value
    
    def is_valid_value(self, value: Any) -> bool:
        """Check if a value is valid for this enum"""
        return value in self._values.values() or value in self._values

# Create VEX enum types
DIRECTION_TYPE = EnumType("DirectionType", {
    "FORWARD": 0,
    "REVERSE": 1
})

TURN_TYPE = EnumType("TurnType", {
    "LEFT": 0,
    "RIGHT": 1
})

BRAKE_TYPE = EnumType("BrakeType", {
    "COAST": 0,
    "BRAKE": 1,
    "HOLD": 2
})

VELOCITY_UNITS = EnumType("VelocityUnits", {
    "PCT": 0,       # Percentage
    "RPM": 1,       # Revolutions per minute
    "DPS": 2        # Degrees per second
})

ROTATION_UNITS = EnumType("RotationUnits", {
    "DEG": 0,       # Degrees
    "REV": 1,       # Revolutions
    "RAW": 2        # Raw data
})

TIME_UNITS = EnumType("TimeUnits", {
    "SEC": 0,       # Seconds
    "MSEC": 1       # Milliseconds
})

DISTANCE_UNITS = EnumType("DistanceUnits", {
    "MM": 0,        # Millimeters
    "IN": 1         # Inches
})

CURRENT_UNITS = EnumType("CurrentUnits", {
    "AMP": 0        # Amperes
})

TORQUE_UNITS = EnumType("TorqueUnits", {
    "NM": 0,        # Newton meters
    "INLB": 1       # Inch pounds
})

TEMPERATURE_UNITS = EnumType("TemperatureUnits", {
    "CELSIUS": 0,
    "FAHRENHEIT": 1
})

ANALOG_UNITS = EnumType("AnalogUnits", {
    "PCT": 0,       # Percentage
    "EIGHTBIT": 1,  # 8-bit (0-255)
    "TENBIT": 2,    # 10-bit (0-1023)
    "TWELVEBIT": 3, # 12-bit (0-4095)
    "MV": 4         # Millivolts
})

# Port type enum
PORT_TYPE = EnumType("PortType", {
    "PORT1": 1,
    "PORT2": 2,
    "PORT3": 3,
    "PORT4": 4,
    "PORT5": 5,
    "PORT6": 6,
    "PORT7": 7,
    "PORT8": 8,
    "PORT9": 9,
    "PORT10": 10,
    "PORT11": 11,
    "PORT12": 12,
    "PORT13": 13,
    "PORT14": 14,
    "PORT15": 15,
    "PORT16": 16,
    "PORT17": 17,
    "PORT18": 18,
    "PORT19": 19,
    "PORT20": 20,
    "PORT21": 21
})

# Add more VEX enum types as needed
