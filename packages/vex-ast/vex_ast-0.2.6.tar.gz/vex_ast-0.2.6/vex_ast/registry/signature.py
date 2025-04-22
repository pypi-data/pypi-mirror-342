from typing import Optional, List, Dict, Any, Union, Callable, Tuple
from enum import Enum, auto
from ..types.base import VexType, VOID, ANY
from .categories import VexCategory, BehaviorType, SubCategory

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
    
    @property
    def optional(self) -> bool:
        """Alias for is_optional for compatibility."""
        return self.is_optional
    
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

# For backward compatibility
class SimulationCategory(Enum):
    """Categories for simulation behavior (deprecated, use VexCategory and BehaviorType instead)"""
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
                 category: Union[VexCategory, SimulationCategory] = None,
                 behavior: BehaviorType = None,
                 subcategory: Optional[SubCategory] = None,
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
        
        # Handle category and behavior
        from .categories import categorizer
        
        # For backward compatibility with SimulationCategory
        if isinstance(category, SimulationCategory):
            # Convert SimulationCategory to BehaviorType
            sim_cat_name = category.name
            self._simulation_category = category  # Store original for backward compatibility
            
            # Determine category and behavior from function name and description
            self.category, self.behavior, self.subcategory = categorizer.categorize_function(
                name, description
            )
            
            # Override behavior based on simulation category mapping
            if sim_cat_name in categorizer.simulation_to_behavior:
                self.behavior = categorizer.simulation_to_behavior[sim_cat_name]
        else:
            # Use provided category and behavior or determine from function name
            if category is None or behavior is None:
                self.category, self.behavior, self.subcategory = categorizer.categorize_function(
                    name, description
                )
                if category is not None:
                    self.category = category
                if behavior is not None:
                    self.behavior = behavior
                if subcategory is not None:
                    self.subcategory = subcategory
            else:
                self.category = category
                self.behavior = behavior
                self.subcategory = subcategory
            
            # For backward compatibility, map to SimulationCategory
            if self.behavior == BehaviorType.CONTROL and self.category == VexCategory.MOTOR:
                self._simulation_category = SimulationCategory.MOTOR_CONTROL
            elif self.behavior == BehaviorType.READ and self.category == VexCategory.SENSOR:
                self._simulation_category = SimulationCategory.SENSOR_READING
            elif self.behavior == BehaviorType.OUTPUT and self.category == VexCategory.DISPLAY:
                self._simulation_category = SimulationCategory.DISPLAY_OUTPUT
            elif self.behavior == BehaviorType.CONTROL and self.category == VexCategory.TIMING:
                self._simulation_category = SimulationCategory.TIMING_CONTROL
            elif self.category == VexCategory.COMPETITION:
                self._simulation_category = SimulationCategory.COMPETITION
            elif self.behavior == BehaviorType.CONFIG:
                self._simulation_category = SimulationCategory.CONFIGURATION
            elif self.behavior == BehaviorType.EVENT:
                self._simulation_category = SimulationCategory.EVENT_HANDLING
            else:
                self._simulation_category = SimulationCategory.OTHER
        
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
    
    @property
    def simulation_category(self) -> SimulationCategory:
        """Get the simulation category (for backward compatibility)"""
        if hasattr(self, '_simulation_category'):
            return self._simulation_category
        return SimulationCategory.OTHER
    
    # Alias for backward compatibility
    @property
    def category(self) -> Union[VexCategory, SimulationCategory]:
        """Get the category (for backward compatibility)"""
        return self.simulation_category
    
    @category.setter
    def category(self, value: Union[VexCategory, SimulationCategory]):
        """Set the category"""
        if isinstance(value, SimulationCategory):
            # For backward compatibility
            self._simulation_category = value
        else:
            # New category system
            self.vex_category = value
    
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
        
        # Type checking for arguments
        from ..types.type_checker import type_checker
        from ..types.enums import EnumType
        
        # Check positional arguments
        for i, arg in enumerate(args):
            if i >= len(self.parameters):
                break
                
            param = self.parameters[i]
            expected_type = param.type
            
            # Handle string literals for enum types
            if isinstance(expected_type, EnumType) and isinstance(arg, str):
                if arg not in expected_type.values:
                    return False, f"Invalid enum value '{arg}' for parameter '{param.name}' in {self.name}"
                continue
                
            # Handle other types
            if hasattr(arg, 'get_type'):
                arg_type = arg.get_type()
                if arg_type and not type_checker.is_compatible(arg_type, expected_type):
                    return False, f"Type mismatch for parameter '{param.name}' in {self.name}: expected {expected_type}, got {arg_type}"
        
        # Check keyword arguments
        for kwarg_name, kwarg_value in kwargs.items():
            # Find the parameter
            param = next((p for p in self.parameters if p.name == kwarg_name), None)
            if not param:
                continue  # Already checked for unknown kwargs above
                
            expected_type = param.type
            
            # Handle string literals for enum types
            if isinstance(expected_type, EnumType) and isinstance(kwarg_value, str):
                if kwarg_value not in expected_type.values:
                    return False, f"Invalid enum value '{kwarg_value}' for parameter '{param.name}' in {self.name}"
                continue
                
            # Handle other types
            if hasattr(kwarg_value, 'get_type'):
                kwarg_type = kwarg_value.get_type()
                if kwarg_type and not type_checker.is_compatible(kwarg_type, expected_type):
                    return False, f"Type mismatch for parameter '{param.name}' in {self.name}: expected {expected_type}, got {kwarg_type}"
        
        return True, None
