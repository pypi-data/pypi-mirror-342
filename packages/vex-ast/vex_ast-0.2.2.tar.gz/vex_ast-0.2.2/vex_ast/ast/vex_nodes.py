"""VEX V5-specific AST nodes with registry integration."""

from typing import Dict, List, Optional, cast, Tuple, Any
from enum import Enum, auto

from .interfaces import IAstNode, IExpression, IVisitor, T_VisitorResult, IFunctionCall
from .expressions import FunctionCall, KeywordArgument
from ..utils.source_location import SourceLocation
from ..registry.api import registry_api
from ..registry.signature import VexFunctionSignature, SimulationCategory

class VexAPICallType(Enum):
    """Types of VEX API calls for classification"""
    MOTOR_CONTROL = auto()
    SENSOR_READING = auto()
    TIMING_CONTROL = auto()
    DISPLAY_OUTPUT = auto()
    BRAIN_FUNCTION = auto()
    CONTROLLER_FUNCTION = auto()
    COMPETITION = auto()
    OTHER = auto()

class VexAPICall(FunctionCall):
    """Base class for VEX API function calls."""
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None,
                 call_type: VexAPICallType = VexAPICallType.OTHER):
        super().__init__(function, args, keywords, location)
        self.call_type = call_type
        self._signature: Optional[VexFunctionSignature] = None
        self._validation_error: Optional[str] = None
    
    def get_function_name(self) -> Optional[str]:
        """Get the function name if available"""
        if hasattr(self.function, 'name'):
            return self.function.name
        
        # Try to handle attribute access (e.g., motor.spin)
        if hasattr(self.function, 'attribute') and hasattr(self.function, 'object'):
            obj = self.function.object
            attr = self.function.attribute
            if hasattr(obj, 'name'):
                return f"{obj.name}.{attr}"
        
        return None
    
    def resolve_signature(self) -> Optional[VexFunctionSignature]:
        """Resolve the function signature from the registry"""
        if self._signature:
            return self._signature
        
        function_name = self.get_function_name()
        if not function_name:
            return None
        
        # Try to get signature from registry API
        if '.' in function_name:
            # For method calls like "motor1.spin", extract the method name
            obj_name, method_name = function_name.split('.', 1)
            
            # First try to get the method signature directly
            self._signature = registry_api.get_function(method_name)
            
            # If that fails, try to get it as a method of a specific object type
            # This is a fallback since we don't know the actual type at parse time
            if not self._signature:
                # Try common object types
                from ..types.objects import MOTOR, TIMER, BRAIN, CONTROLLER
                for obj_type in [MOTOR, TIMER, BRAIN, CONTROLLER]:
                    method_sig = registry_api.get_method(obj_type, method_name)
                    if method_sig:
                        self._signature = method_sig
                        break
        else:
            # For direct function calls
            self._signature = registry_api.get_function(function_name)
            
        return self._signature
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate this function call against the registry"""
        if self._validation_error:
            return False, self._validation_error
        
        signature = self.resolve_signature()
        if not signature:
            function_name = self.get_function_name() or "<unknown>"
            self._validation_error = f"Unknown VEX function: {function_name}"
            return False, self._validation_error
        
        # Convert args and kwargs to appropriate format
        arg_values = [arg for arg in self.args]
        kwarg_values = {kw.name: kw.value for kw in self.keywords or []}
        
        # Validate against the signature
        valid, error = signature.validate_arguments(arg_values, kwarg_values)
        if not valid:
            self._validation_error = error
        
        return valid, error
    
    def get_simulation_category(self) -> Optional[SimulationCategory]:
        """Get the simulation category for this function call"""
        signature = self.resolve_signature()
        if signature:
            return signature.category
        return None
    
    def get_call_type(self) -> VexAPICallType:
        """Get the call type of this VEX API call."""
        return self.call_type
    
    def get_signature(self) -> Optional[VexFunctionSignature]:
        """Get the function signature if resolved."""
        return self._signature
    
    def get_validation_error(self) -> Optional[str]:
        """Get the validation error if any."""
        return self._validation_error
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_vexapicall(self)

class MotorControl(VexAPICall):
    """A VEX motor control function call."""
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(function, args, keywords, location, VexAPICallType.MOTOR_CONTROL)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_motorcontrol(self)
    
    def get_motor_name(self) -> Optional[str]:
        """Get the motor name if this is a method call on a motor object."""
        function_name = self.get_function_name()
        if function_name and '.' in function_name:
            return function_name.split('.', 1)[0]
        return None

class SensorReading(VexAPICall):
    """A VEX sensor reading function call."""
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(function, args, keywords, location, VexAPICallType.SENSOR_READING)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_sensorreading(self)
    
    def get_sensor_name(self) -> Optional[str]:
        """Get the sensor name if this is a method call on a sensor object."""
        function_name = self.get_function_name()
        if function_name and '.' in function_name:
            return function_name.split('.', 1)[0]
        return None

class TimingControl(VexAPICall):
    """A VEX timing control function call."""
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(function, args, keywords, location, VexAPICallType.TIMING_CONTROL)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_timingcontrol(self)
    
    def get_timing_method(self) -> Optional[str]:
        """Get the timing method name."""
        function_name = self.get_function_name()
        if function_name and '.' in function_name:
            return function_name.split('.', 1)[1]
        return function_name

class DisplayOutput(VexAPICall):
    """A VEX display output function call."""
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(function, args, keywords, location, VexAPICallType.DISPLAY_OUTPUT)
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_displayoutput(self)
    
    def get_display_method(self) -> Optional[str]:
        """Get the display method name."""
        function_name = self.get_function_name()
        if function_name and '.' in function_name:
            return function_name.split('.', 1)[1]
        return function_name

def create_vex_api_call(function: IExpression, args: List[IExpression],
                       keywords: List[KeywordArgument] = None,
                       location: Optional[SourceLocation] = None) -> VexAPICall:
    """Factory function to create the appropriate VEX API call node"""
    # Determine the function name
    function_name = None
    if hasattr(function, 'name'):
        function_name = function.name
    elif hasattr(function, 'attribute') and hasattr(function, 'object'):
        obj = function.object
        attr = function.attribute
        if hasattr(obj, 'name'):
            function_name = f"{obj.name}.{attr}"
    
    # If we can't determine the function name, return a generic VexAPICall
    if not function_name:
        return VexAPICall(function, args, keywords, location)
    
    # Look up in the registry API to get the function category
    signature = None
    if '.' in function_name:
        # For method calls like "motor1.spin", extract the method name
        obj_name, method_name = function_name.split('.', 1)
        
        # First try to get the method signature directly
        signature = registry_api.get_function(method_name)
        
        # If that fails, try to get it as a method of a specific object type
        if not signature:
            # Try common object types
            from ..types.objects import MOTOR, TIMER, BRAIN, CONTROLLER
            for obj_type in [MOTOR, TIMER, BRAIN, CONTROLLER]:
                method_sig = registry_api.get_method(obj_type, method_name)
                if method_sig:
                    signature = method_sig
                    break
    else:
        # For direct function calls
        signature = registry_api.get_function(function_name)
        
    if not signature:
        return VexAPICall(function, args, keywords, location)
    
    # Create the appropriate node type based on the simulation category
    if signature.category == SimulationCategory.MOTOR_CONTROL:
        return MotorControl(function, args, keywords, location)
    elif signature.category == SimulationCategory.SENSOR_READING:
        return SensorReading(function, args, keywords, location)
    elif signature.category == SimulationCategory.TIMING_CONTROL:
        return TimingControl(function, args, keywords, location)
    elif signature.category == SimulationCategory.DISPLAY_OUTPUT:
        return DisplayOutput(function, args, keywords, location)
    
    # Default case
    return VexAPICall(function, args, keywords, location)

# Factory function to create VEX API calls from interfaces
def create_vex_api_call_from_interface(function_expr: IExpression, 
                                      args: List[IExpression],
                                      kwargs: Dict[str, IExpression] = None,
                                      location: Optional[SourceLocation] = None) -> VexAPICall:
    """Create a VEX API call from interface types."""
    # Convert kwargs to KeywordArgument objects
    keywords = []
    if kwargs:
        for name, value in kwargs.items():
            keywords.append(KeywordArgument(name, value))
    
    return create_vex_api_call(function_expr, args, keywords, location)
