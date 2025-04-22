from typing import Dict, List, Optional, Set, Tuple, Any, Union
from enum import Enum
from .signature import VexFunctionSignature, VexFunctionParameter, SimulationCategory
from ..types.base import VexType
from .categories import FunctionCategory, SubCategory, categorizer
from .language_map import language_mapper
from .simulation_behavior import SimulationBehavior

class VexFunctionRegistry:
    """Registry for storing and retrieving VEX function signatures"""
    
    _instance = None
    
    @classmethod
    def register(cls, signature: VexFunctionSignature) -> None:
        """Static method to register a function signature in the registry"""
        instance = cls()
        instance.register_function(signature)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VexFunctionRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the registry"""
        self.functions: Dict[str, VexFunctionSignature] = {}
        self.functions_by_category: Dict[FunctionCategory, List[VexFunctionSignature]] = {}
        self.functions_by_subcategory: Dict[SubCategory, List[VexFunctionSignature]] = {}
        self.functions_by_simulation: Dict[SimulationCategory, List[VexFunctionSignature]] = {}
        self.method_map: Dict[Tuple[str, str], VexFunctionSignature] = {}  # (object_type, method_name) -> signature
        
        # Initialize category dictionaries
        for category in FunctionCategory:
            self.functions_by_category[category] = []
        
        for subcategory in SubCategory:
            self.functions_by_subcategory[subcategory] = []
        
        for sim_category in SimulationCategory:
            self.functions_by_simulation[sim_category] = []
    
    def register_function(self, signature: VexFunctionSignature) -> None:
        """Register a function signature in the registry"""
        # Register by name
        self.functions[signature.name] = signature
        
        # Register Python and C++ name variations
        if signature.python_name and signature.python_name != signature.name:
            self.functions[signature.python_name] = signature
        
        if signature.cpp_name and signature.cpp_name != signature.name:
            self.functions[signature.cpp_name] = signature
        
        # Register by simulation category
        self.functions_by_simulation[signature.category].append(signature)
        
        # Categorize function
        category, subcategory = categorizer.categorize_function(
            signature.name, signature.description
        )
        
        # Register by category
        self.functions_by_category[category].append(signature)
        
        # Register by subcategory if available
        if subcategory:
            self.functions_by_subcategory[subcategory].append(signature)
        
        # Register as method if applicable
        if signature.object_type and signature.method_name:
            key = (signature.object_type.name, signature.method_name)
            self.method_map[key] = signature
    
    def get_function(self, 
                    name: str, 
                    language: str = "python") -> Optional[VexFunctionSignature]:
        """Get a function signature by name"""
        # Try direct lookup
        if name in self.functions:
            return self.functions[name]
        
        # Try language-specific lookup
        if language == "cpp":
            python_name = language_mapper.get_python_name(name)
            if python_name and python_name in self.functions:
                return self.functions[python_name]
        elif language == "python":
            cpp_name = language_mapper.get_cpp_name(name)
            if cpp_name and cpp_name in self.functions:
                return self.functions[cpp_name]
        
        return None
    
    def get_method(self, 
                  object_type: Union[VexType, str], 
                  method_name: str) -> Optional[VexFunctionSignature]:
        """Get a method signature for an object type and method name"""
        type_name = object_type.name if hasattr(object_type, 'name') else str(object_type)
        key = (type_name, method_name)
        return self.method_map.get(key)
    
    def get_functions_by_category(self, category: FunctionCategory) -> List[VexFunctionSignature]:
        """Get all functions in a category"""
        return self.functions_by_category.get(category, [])
    
    def get_functions_by_subcategory(self, subcategory: SubCategory) -> List[VexFunctionSignature]:
        """Get all functions in a subcategory"""
        return self.functions_by_subcategory.get(subcategory, [])
    
    def get_functions_by_simulation(self, 
                                  sim_category: SimulationCategory) -> List[VexFunctionSignature]:
        """Get all functions with a specific simulation category"""
        return self.functions_by_simulation.get(sim_category, [])
    
    def validate_call(self, 
                     function_name: str, 
                     args: List[Any],
                     kwargs: Dict[str, Any],
                     language: str = "python") -> Tuple[bool, Optional[str]]:
        """Validate a function call"""
        # Get the function signature
        signature = self.get_function(function_name, language)
        if not signature:
            return False, f"Unknown function: {function_name}"
        
        # Validate arguments
        return signature.validate_arguments(args, kwargs)
    
    def validate_method_call(self,
                           object_type: Union[VexType, str],
                           method_name: str,
                           args: List[Any],
                           kwargs: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate a method call on an object"""
        # Get the method signature
        signature = self.get_method(object_type, method_name)
        if not signature:
            type_name = object_type.name if hasattr(object_type, 'name') else str(object_type)
            return False, f"Unknown method {method_name} for type {type_name}"
        
        # Validate arguments
        return signature.validate_arguments(args, kwargs)
    
    def get_all_functions(self) -> List[VexFunctionSignature]:
        """Get all registered functions"""
        # Use set to remove duplicates since a function can be registered multiple times
        # with different names
        return list(set(self.functions.values()))

# Singleton instance
registry = VexFunctionRegistry()
