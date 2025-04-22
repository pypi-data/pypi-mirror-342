from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID, ANY
from ...types.primitives import INT, FLOAT, BOOL
from ...types.enums import TIME_UNITS
from ...types.objects import TIMER

def register_timing_functions():
    """Register timing-related functions in the registry"""
    
    # Global wait function
    wait_params = [
        VexFunctionParameter("time", FLOAT, description="Time to wait"),
        VexFunctionParameter("units", TIME_UNITS, "MSEC", description="Time units")
    ]
    
    wait_signature = VexFunctionSignature(
        name="wait",
        return_type=VOID,
        parameters=wait_params,
        description="Wait for a specified amount of time",
        category=SimulationCategory.TIMING_CONTROL,
        python_name="wait",
        cpp_name="wait"
    )
    
    registry.register_function(wait_signature)
    
    # Timer functions
    
    # Timer.time() method
    time_params = [
        VexFunctionParameter("units", TIME_UNITS, "MSEC", description="Time units")
    ]
    
    time_signature = VexFunctionSignature(
        name="time",
        return_type=FLOAT,
        parameters=time_params,
        description="Get the current time of the timer",
        category=SimulationCategory.TIMING_CONTROL,
        python_name="time",
        cpp_name="time",
        object_type=TIMER,
        method_name="time"
    )
    
    registry.register_function(time_signature)
    
    # Timer.clear() method
    clear_signature = VexFunctionSignature(
        name="clear",
        return_type=VOID,
        parameters=[],
        description="Clear the timer",
        category=SimulationCategory.TIMING_CONTROL,
        python_name="clear",
        cpp_name="clear",
        object_type=TIMER,
        method_name="clear"
    )
    
    registry.register_function(clear_signature)
    
    # Timer.reset() method
    reset_signature = VexFunctionSignature(
        name="reset",
        return_type=VOID,
        parameters=[],
        description="Reset the timer",
        category=SimulationCategory.TIMING_CONTROL,
        python_name="reset",
        cpp_name="reset",
        object_type=TIMER,
        method_name="reset"
    )
    
    registry.register_function(reset_signature)
    
    # Timer.event() method
    event_params = [
        VexFunctionParameter("callback", ANY, description="Callback function to execute"),
        VexFunctionParameter("delay", FLOAT, description="Time delay before callback execution"),
        VexFunctionParameter("units", TIME_UNITS, "MSEC", description="Time units")
    ]
    
    event_signature = VexFunctionSignature(
        name="event",
        return_type=VOID,
        parameters=event_params,
        description="Register a callback function to be called after a delay",
        category=SimulationCategory.EVENT_HANDLING,
        python_name="event",
        cpp_name="event",
        object_type=TIMER,
        method_name="event"
    )
    
    registry.register_function(event_signature)
    
    # Add more timing functions as needed...

if __name__ == "__main__":
    register_timing_functions()