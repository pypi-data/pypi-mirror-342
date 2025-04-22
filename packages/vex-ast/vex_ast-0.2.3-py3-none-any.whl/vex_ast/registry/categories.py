from enum import Enum, auto
from typing import Set, Dict, List, Optional, Tuple

class FunctionCategory(Enum):
    """Categories for VEX functions"""
    MOTOR = auto()             # Motor control functions
    DRIVETRAIN = auto()        # Drivetrain control functions
    SENSOR = auto()            # Sensor reading functions
    DISPLAY = auto()           # Display output functions
    TIMING = auto()            # Timing control functions
    COMPETITION = auto()       # Competition control functions
    CONTROLLER = auto()        # Controller input functions
    BRAIN = auto()             # Brain functions
    UTILITY = auto()           # Utility functions
    EVENT = auto()             # Event handling
    OTHER = auto()             # Other functions

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
        self.category_patterns: Dict[FunctionCategory, List[str]] = {
            FunctionCategory.MOTOR: ["motor", "spin", "velocity", "torque", "efficiency"],
            FunctionCategory.DRIVETRAIN: ["drive", "turn", "drivetrain"],
            FunctionCategory.SENSOR: ["sensor", "distance", "inertial", "rotation", "optical", "vision", "limit", "bumper", "gps"],
            FunctionCategory.DISPLAY: ["display", "print", "draw", "screen", "clear"],
            FunctionCategory.TIMING: ["wait", "sleep", "delay", "timer"],
            FunctionCategory.COMPETITION: ["competition", "autonomous", "driver"],
            FunctionCategory.CONTROLLER: ["controller", "button", "joystick", "rumble"],
            FunctionCategory.BRAIN: ["brain", "battery"],
            FunctionCategory.UTILITY: ["random", "math", "color"],
            FunctionCategory.EVENT: ["event", "callback", "when", "register"],
        }
        
        self.subcategory_patterns: Dict[SubCategory, List[str]] = {
            # Motor subcategories
            SubCategory.MOTOR_SPIN: ["spin", "rotate"],
            SubCategory.MOTOR_STOP: ["stop", "brake"],
            SubCategory.MOTOR_CONFIGURATION: ["set_", "configure"],
            SubCategory.MOTOR_MEASUREMENT: ["current", "temperature", "velocity", "position"],
            
            # Additional subcategory patterns can be added as needed
        }
    
    def categorize_function(self, 
                           function_name: str, 
                           description: str = "") -> Tuple[FunctionCategory, Optional[SubCategory]]:
        """Categorize a function based on its name and description"""
        function_name = function_name.lower()
        description = description.lower()
        
        # Try to find the main category
        category = FunctionCategory.OTHER
        for cat, patterns in self.category_patterns.items():
            for pattern in patterns:
                if pattern in function_name or pattern in description:
                    category = cat
                    break
            if category != FunctionCategory.OTHER:
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
        
        return category, subcategory

# Singleton instance
categorizer = FunctionCategorizer()