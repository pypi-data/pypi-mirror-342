from enum import Enum, auto, StrEnum
from typing import Set, Dict, List, Optional, Tuple

class VexCategory(StrEnum):
    """Categories for VEX functions"""
    MOTOR = "MOTOR"             # Motor control functions
    DRIVETRAIN = "DRIVETRAIN"   # Drivetrain control functions
    SENSOR = "SENSOR"           # Sensor reading functions
    DISPLAY = "DISPLAY"         # Display output functions
    TIMING = "TIMING"           # Timing control functions
    COMPETITION = "COMPETITION" # Competition control functions
    CONTROLLER = "CONTROLLER"   # Controller input functions
    BRAIN = "BRAIN"             # Brain functions
    UTILITY = "UTILITY"         # Utility functions
    EVENT = "EVENT"             # Event handling
    OTHER = "OTHER"             # Other functions

class BehaviorType(StrEnum):
    """Behavior types for VEX functions"""
    CONTROL = "CONTROL"         # Actively controls/changes state
    READ = "READ"               # Reads/retrieves information
    CONFIG = "CONFIG"           # Configuration/setup
    OUTPUT = "OUTPUT"           # Produces output (display, signals)
    EVENT = "EVENT"             # Event handling/callbacks
    OTHER = "OTHER"             # Other behaviors

# For backward compatibility
FunctionCategory = VexCategory

class SubCategory(Enum):
    """Subcategories for more fine-grained classification"""
    # Motor subcategories
    MOTOR_SPIN = auto()
    MOTOR_STOP = auto()
    MOTOR_CONFIGURATION = auto()
    MOTOR_MEASUREMENT = auto()
    
    # Drivetrain subcategories
    DRIVE_MOVEMENT = auto()
    DRIVE_TURN = auto()
    DRIVE_CONFIGURATION = auto()
    
    # Sensor subcategories
    DISTANCE_SENSOR = auto()
    INERTIAL_SENSOR = auto()
    ROTATION_SENSOR = auto()
    OPTICAL_SENSOR = auto()
    VISION_SENSOR = auto()
    LIMIT_SWITCH = auto()
    BUMPER = auto()
    GPS_SENSOR = auto()
    
    # Display subcategories
    SCREEN_DRAWING = auto()
    SCREEN_TEXT = auto()
    SCREEN_CLEARING = auto()
    
    # Timing subcategories
    WAIT = auto()
    TIMER = auto()
    
    # Competition subcategories
    COMPETITION_STATUS = auto()
    COMPETITION_CONTROL = auto()
    
    # Controller subcategories
    BUTTON_INPUT = auto()
    JOYSTICK_INPUT = auto()
    CONTROLLER_SCREEN = auto()
    CONTROLLER_RUMBLE = auto()
    
    # Brain subcategories
    BRAIN_BATTERY = auto()
    BRAIN_SCREEN = auto()
    BRAIN_BUTTONS = auto()
    BRAIN_SD_CARD = auto()
    
    # Utility subcategories
    MATH = auto()
    RANDOM = auto()
    COLOR = auto()
    
    # Event subcategories
    CALLBACK = auto()
    EVENT_REGISTRATION = auto()
    
    # Other subcategories
    SYSTEM = auto()
    DEBUGGING = auto()

class FunctionCategorizer:
    """Utility for categorizing VEX functions"""
    
    def __init__(self):
        self.category_patterns: Dict[VexCategory, List[str]] = {
            VexCategory.MOTOR: ["motor", "spin", "velocity", "torque", "efficiency"],
            VexCategory.DRIVETRAIN: ["drive", "turn", "drivetrain"],
            VexCategory.SENSOR: ["sensor", "distance", "inertial", "rotation", "optical", "vision", "limit", "bumper", "gps"],
            VexCategory.DISPLAY: ["display", "print", "draw", "screen", "clear"],
            VexCategory.TIMING: ["wait", "sleep", "delay", "timer"],
            VexCategory.COMPETITION: ["competition", "autonomous", "driver"],
            VexCategory.CONTROLLER: ["controller", "button", "joystick", "rumble"],
            VexCategory.BRAIN: ["brain", "battery"],
            VexCategory.UTILITY: ["random", "math", "color"],
            VexCategory.EVENT: ["event", "callback", "when", "register"],
        }
        
        self.behavior_patterns: Dict[BehaviorType, List[str]] = {
            BehaviorType.CONTROL: ["spin", "drive", "turn", "stop", "brake", "set", "clear"],
            BehaviorType.READ: ["get", "read", "measure", "is_", "has_", "current", "temperature", "position"],
            BehaviorType.CONFIG: ["configure", "calibrate", "initialize", "setup"],
            BehaviorType.OUTPUT: ["print", "draw", "display", "rumble"],
            BehaviorType.EVENT: ["event", "callback", "when", "register", "handler"],
        }
        
        self.subcategory_patterns: Dict[SubCategory, List[str]] = {
            # Motor subcategories
            SubCategory.MOTOR_SPIN: ["spin", "rotate"],
            SubCategory.MOTOR_STOP: ["stop", "brake"],
            SubCategory.MOTOR_CONFIGURATION: ["set_", "configure"],
            SubCategory.MOTOR_MEASUREMENT: ["current", "temperature", "velocity", "position"],
            
            # Additional subcategory patterns can be added as needed
        }
        
        # Mapping from old SimulationCategory to new BehaviorType
        self.simulation_to_behavior = {
            "MOTOR_CONTROL": BehaviorType.CONTROL,
            "SENSOR_READING": BehaviorType.READ,
            "DISPLAY_OUTPUT": BehaviorType.OUTPUT,
            "TIMING_CONTROL": BehaviorType.CONTROL,
            "COMPETITION": BehaviorType.OTHER,
            "CONFIGURATION": BehaviorType.CONFIG,
            "CALCULATION": BehaviorType.OTHER,
            "EVENT_HANDLING": BehaviorType.EVENT,
            "OTHER": BehaviorType.OTHER
        }
    
    def categorize_function(self, 
                           function_name: str, 
                           description: str = "") -> Tuple[VexCategory, BehaviorType, Optional[SubCategory]]:
        """Categorize a function based on its name and description"""
        function_name = function_name.lower()
        description = description.lower()
        
        # Try to find the main category
        category = VexCategory.OTHER
        for cat, patterns in self.category_patterns.items():
            for pattern in patterns:
                if pattern in function_name or pattern in description:
                    category = cat
                    break
            if category != VexCategory.OTHER:
                break
        
        # Try to find the behavior type
        behavior = BehaviorType.OTHER
        for behav, patterns in self.behavior_patterns.items():
            for pattern in patterns:
                if pattern in function_name or pattern in description:
                    behavior = behav
                    break
            if behavior != BehaviorType.OTHER:
                break
        
        # Try to find the subcategory
        subcategory = None
        for subcat, patterns in self.subcategory_patterns.items():
            for pattern in patterns:
                if pattern in function_name or pattern in description:
                    subcategory = subcat
                    break
            if subcategory:
                break
        
        return category, behavior, subcategory

# Singleton instance
categorizer = FunctionCategorizer()
