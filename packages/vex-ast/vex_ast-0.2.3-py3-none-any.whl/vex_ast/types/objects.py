from typing import Optional, List, Dict, Any, Set, TYPE_CHECKING
from .base import VexType, type_registry

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from ..registry.signature import VexFunctionSignature

class ObjectType(VexType):
    """Base class for all VEX object types (motors, sensors, etc.)"""
    
    def __init__(self, name: str, methods: Dict[str, 'VexFunctionSignature'] = None):
        self._name = name
        self._methods = methods or {}
        type_registry.register_type(self)
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def methods(self) -> Dict[str, Any]:  # Use Any instead of forward reference
        return self._methods
    
    def add_method(self, method_name: str, signature: Any) -> None:  # Use Any instead of forward reference
        """Add a method to this object type"""
        self._methods[method_name] = signature
    
    def get_method(self, method_name: str) -> Optional[Any]:  # Use Any instead of forward reference
        """Get a method by name"""
        return self._methods.get(method_name)
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Objects are compatible only with the same type"""
        return isinstance(other, ObjectType) and self.name == other.name
    
    def __str__(self) -> str:
        return self._name

# VEX object types - define basic types here, methods will be added later
MOTOR = ObjectType("Motor")
MOTOR_GROUP = ObjectType("MotorGroup")
DRIVETRAIN = ObjectType("Drivetrain")
BRAIN = ObjectType("Brain")
CONTROLLER = ObjectType("Controller")
INERTIAL = ObjectType("Inertial")
DISTANCE = ObjectType("Distance")
ROTATION = ObjectType("Rotation")
OPTICAL = ObjectType("Optical")
GPS = ObjectType("GPS")
ELECTROMAGNETIC = ObjectType("Electromagnetic")
BRAIN_BATTERY = ObjectType("BrainBattery")
BRAIN_SCREEN = ObjectType("BrainScreen")
BRAIN_LCD = ObjectType("BrainLcd")
COMPETITION = ObjectType("Competition")
TIMER = ObjectType("Timer")
BUMPER = ObjectType("Bumper")
LIMIT_SWITCH = ObjectType("LimitSwitch")
ENCODER = ObjectType("Encoder")
SONAR = ObjectType("Sonar")
GYRO = ObjectType("Gyro")
PNEUMATIC = ObjectType("Pneumatic")
VISION = ObjectType("Vision")

# Add additional object types as needed
