from ..registry import registry
from ..signature import VexFunctionSignature, VexFunctionParameter, ParameterMode, SimulationCategory
from ...types.base import VOID, ANY
from ...types.primitives import INT, FLOAT, BOOL, STRING
from ...types.objects import BRAIN_SCREEN, CONTROLLER

def register_display_functions():
    """Register display-related functions in the registry"""
    
    # Brain screen functions
    
    # Brain.Screen.print() method
    print_params = [
        VexFunctionParameter("text", ANY, description="Text to print")
    ]
    
    print_signature = VexFunctionSignature(
        name="print",
        return_type=VOID,
        parameters=print_params,
        description="Print text to the brain screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="print",
        cpp_name="print",
        object_type=BRAIN_SCREEN,
        method_name="print"
    )
    
    registry.register_function(print_signature)
    
    # Brain.Screen.clear_screen() method
    clear_screen_signature = VexFunctionSignature(
        name="clear_screen",
        return_type=VOID,
        parameters=[],
        description="Clear the brain screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="clear_screen",
        cpp_name="clearScreen",
        object_type=BRAIN_SCREEN,
        method_name="clear_screen"
    )
    
    registry.register_function(clear_screen_signature)
    
    # Brain.Screen.set_cursor() method
    set_cursor_params = [
        VexFunctionParameter("row", INT, description="Row position"),
        VexFunctionParameter("col", INT, description="Column position")
    ]
    
    set_cursor_signature = VexFunctionSignature(
        name="set_cursor",
        return_type=VOID,
        parameters=set_cursor_params,
        description="Set the cursor position on the brain screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="set_cursor",
        cpp_name="setCursor",
        object_type=BRAIN_SCREEN,
        method_name="set_cursor"
    )
    
    registry.register_function(set_cursor_signature)
    
    # Brain.Screen.draw_pixel() method
    draw_pixel_params = [
        VexFunctionParameter("x", INT, description="X coordinate"),
        VexFunctionParameter("y", INT, description="Y coordinate")
    ]
    
    draw_pixel_signature = VexFunctionSignature(
        name="draw_pixel",
        return_type=VOID,
        parameters=draw_pixel_params,
        description="Draw a pixel on the brain screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="draw_pixel",
        cpp_name="drawPixel",
        object_type=BRAIN_SCREEN,
        method_name="draw_pixel"
    )
    
    registry.register_function(draw_pixel_signature)
    
    # Brain.Screen.draw_line() method
    draw_line_params = [
        VexFunctionParameter("x1", INT, description="Start X coordinate"),
        VexFunctionParameter("y1", INT, description="Start Y coordinate"),
        VexFunctionParameter("x2", INT, description="End X coordinate"),
        VexFunctionParameter("y2", INT, description="End Y coordinate")
    ]
    
    draw_line_signature = VexFunctionSignature(
        name="draw_line",
        return_type=VOID,
        parameters=draw_line_params,
        description="Draw a line on the brain screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="draw_line",
        cpp_name="drawLine",
        object_type=BRAIN_SCREEN,
        method_name="draw_line"
    )
    
    registry.register_function(draw_line_signature)
    
    # Controller screen functions (V5 Controller)
    
    # Controller.Screen.print() method
    controller_print_params = [
        VexFunctionParameter("text", ANY, description="Text to print")
    ]
    
    controller_print_signature = VexFunctionSignature(
        name="print",
        return_type=VOID,
        parameters=controller_print_params,
        description="Print text to the controller screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="print",
        cpp_name="print",
        object_type=CONTROLLER,
        method_name="print"
    )
    
    registry.register_function(controller_print_signature)
    
    # Controller.Screen.clear_screen() method
    controller_clear_screen_signature = VexFunctionSignature(
        name="clear_screen",
        return_type=VOID,
        parameters=[],
        description="Clear the controller screen",
        category=SimulationCategory.DISPLAY_OUTPUT,
        python_name="clear_screen",
        cpp_name="clearScreen",
        object_type=CONTROLLER,
        method_name="clear_screen"
    )
    
    registry.register_function(controller_clear_screen_signature)
    
    # Add more display functions as needed...

if __name__ == "__main__":
    register_display_functions()