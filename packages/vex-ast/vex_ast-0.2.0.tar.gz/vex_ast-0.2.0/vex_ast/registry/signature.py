from typing import Optional, List, Dict, Any, Union, Callable, Tuple
from enum import Enum, auto
from ..types.base import VexType, VOID, ANY

class ParameterMode(Enum):
    """Parameter passing modes"""
    VALUE = auto()      # Pass by value
    REFERENCE = auto()  # Pass by reference
    OUTPUT = auto()     # Output parameter

class VexFunctionParameter:
    """Represents a parameter in a VEX function signature"""
    
    def __init__(self, 
                 name: str, 
                 type_: VexType, 
                 default_value: Optional[Any] = None,
                 mode: ParameterMode = ParameterMode.VALUE,
                 description: str = ""):
        self.name = name
        self.type = type_
        self.default_value = default_value
        self.mode = mode
        self.description = description
        self.is_optional = default_value is not None
    
    def __str__(self) -> str:
        mode_str = ""
        if self.mode == ParameterMode.REFERENCE:
            mode_str = "&"
        elif self.mode == ParameterMode.OUTPUT:
            mode_str = "*"
            
        default_str = ""
        if self.is_optional:
            default_str = f" = {self.default_value}"
            
        return f"{self.type}{mode_str} {self.name}{default_str}"

class SimulationCategory(Enum):
    """Categories for simulation behavior"""
    MOTOR_CONTROL = auto()
    SENSOR_READING = auto()
    DISPLAY_OUTPUT = auto()
    TIMING_CONTROL = auto()
    COMPETITION = auto()
    CONFIGURATION = auto()
    CALCULATION = auto()
    EVENT_HANDLING = auto()
    OTHER = auto()

SimulationBehaviorFunc = Callable[..., Any]

class VexFunctionSignature:
    """Represents the signature of a VEX function"""
    
    def __init__(self, 
                 name: str, 
                 return_type: VexType = VOID,
                 parameters: List[Union[VexFunctionParameter, Tuple[str, str, Optional[Any]]]] = None,
                 description: str = "",
                 category: SimulationCategory = SimulationCategory.OTHER,
                 simulation_behavior: Optional[SimulationBehaviorFunc] = None,
                 python_name: Optional[str] = None,
                 cpp_name: Optional[str] = None,
                 object_type: Optional[VexType] = None,
                 method_name: Optional[str] = None):
        self.name = name
        self.return_type = return_type
        
        # Convert tuple parameters to VexFunctionParameter objects
        processed_params = []
        if parameters:
            for param in parameters:
                if isinstance(param, VexFunctionParameter):
                    processed_params.append(param)
                elif isinstance(param, tuple) and len(param) >= 2:
                    # Extract tuple values
                    param_name = param[0]
                    param_type = param[1]
                    default_value = param[2] if len(param) > 2 else None
                    processed_params.append(VexFunctionParameter(
                        name=param_name,
                        type_=param_type,
                        default_value=default_value
                    ))
        
        self.parameters = processed_params
        self.description = description
        self.category = category
        self.simulation_behavior = simulation_behavior
        self.python_name = python_name or name
        self.cpp_name = cpp_name or name
        self.object_type = object_type  # For methods, this is the class type
        self.method_name = method_name  # For methods, this is the method name
        
        
        # Validate there are no duplicate parameter names
        param_names = [param.name for param in self.parameters]
        if len(param_names) != len(set(param_names)):
            raise ValueError(f"Duplicate parameter names in function {name}")
        
        # Ensure optional parameters come after required parameters
        has_optional = False
        for param in self.parameters:
            if param.is_optional:
                has_optional = True
            elif has_optional:
                raise ValueError(f"Required parameter after optional parameter in function {name}")
    
    def __str__(self) -> str:
        params_str = ", ".join(str(param) for param in self.parameters)
        return f"{self.return_type} {self.name}({params_str})"
    
    def validate_arguments(self, 
                          args: List[Any], 
                          kwargs: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate function arguments against this signature"""
        # Check if we have too many positional arguments
        if len(args) > len(self.parameters):
            return False, f"Too many positional arguments for {self.name}"
        
        # Check if we have unknown keyword arguments
        param_names = {param.name for param in self.parameters}
        for kwarg_name in kwargs:
            if kwarg_name not in param_names:
                return False, f"Unknown keyword argument '{kwarg_name}' for {self.name}"
        
        # Check if we have the required number of arguments
        required_params = [p for p in self.parameters if not p.is_optional]
        if len(args) + len(kwargs) < len(required_params):
            return False, f"Missing required arguments for {self.name}"
        
        # Check if we have duplicate arguments
        args_used = min(len(args), len(self.parameters))
        for i in range(args_used):
            param_name = self.parameters[i].name
            if param_name in kwargs:
                return False, f"Duplicate argument '{param_name}' for {self.name}"
        
        # TODO: Add type checking for arguments
        
        return True, None
