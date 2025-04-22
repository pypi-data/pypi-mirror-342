"""Initialize all VEX function definitions in the registry"""

from . import motor, drivetrain, sensors, timing, display
# Import other function modules as they are added

def initialize_registry():
    """Initialize the registry with all VEX functions"""
    # Motor functions
    motor.register_motor_functions()
    
    # Drivetrain functions
    drivetrain.register_drivetrain_functions()
    
    # Sensor functions
    sensors.register_sensor_functions()
    
    # Timing functions
    timing.register_timing_functions()
    
    # Display functions
    display.register_display_functions()
    
    # Add other function registration calls as modules are added
    
    print("VEX function registry initialized successfully")

if __name__ == "__main__":
    initialize_registry()