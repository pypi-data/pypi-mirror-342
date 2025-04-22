"""API layer for the VEX function registry.

This module provides a clean API for accessing the VEX function registry,
hiding implementation details and providing a more stable interface.
"""

from typing import Dict, List, Optional, Union, Tuple, Any, Set

from .registry import registry, VexFunctionRegistry
from .signature import VexFunctionSignature, SimulationCategory
from .categories import FunctionCategory, SubCategory
from ..types.base import VexType

class RegistryAPI:
    """API layer for the VEX function registry."""
    
    def __init__(self, registry_instance: VexFunctionRegistry = None):
        """Initialize with a registry instance or use the singleton."""
        self._registry = registry_instance or registry
    
    def get_function(self, name: str, language: str = "python") -> Optional[VexFunctionSignature]:
        """Get a function signature by name.
        
        Args:
            name: The function name
            language: The language to use for name resolution ("python" or "cpp")
            
        Returns:
            The function signature if found, None otherwise
        """
        return self._registry.get_function(name, language)
    
    def get_method(self, object_type: Union[VexType, str], 
                  method_name: str) -> Optional[VexFunctionSignature]:
        """Get a method signature for an object type and method name.
        
        Args:
            object_type: The object type or type name
            method_name: The method name
            
        Returns:
            The method signature if found, None otherwise
        """
        return self._registry.get_method(object_type, method_name)
    
    def get_functions_by_category(self, category: FunctionCategory) -> List[VexFunctionSignature]:
        """Get all functions in a category.
        
        Args:
            category: The function category
            
        Returns:
            List of function signatures in the category
        """
        return self._registry.get_functions_by_category(category)
    
    def get_functions_by_subcategory(self, subcategory: SubCategory) -> List[VexFunctionSignature]:
        """Get all functions in a subcategory.
        
        Args:
            subcategory: The function subcategory
            
        Returns:
            List of function signatures in the subcategory
        """
        return self._registry.get_functions_by_subcategory(subcategory)
    
    def get_functions_by_simulation(self, 
                                  sim_category: SimulationCategory) -> List[VexFunctionSignature]:
        """Get all functions with a specific simulation category.
        
        Args:
            sim_category: The simulation category
            
        Returns:
            List of function signatures with the simulation category
        """
        return self._registry.get_functions_by_simulation(sim_category)
    
    def validate_call(self, function_name: str, 
                     args: List[Any],
                     kwargs: Dict[str, Any],
                     language: str = "python") -> Tuple[bool, Optional[str]]:
        """Validate a function call.
        
        Args:
            function_name: The function name
            args: The positional arguments
            kwargs: The keyword arguments
            language: The language to use for name resolution
            
        Returns:
            A tuple of (valid, error_message)
        """
        return self._registry.validate_call(function_name, args, kwargs, language)
    
    def validate_method_call(self, object_type: Union[VexType, str],
                           method_name: str,
                           args: List[Any],
                           kwargs: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate a method call on an object.
        
        Args:
            object_type: The object type or type name
            method_name: The method name
            args: The positional arguments
            kwargs: The keyword arguments
            
        Returns:
            A tuple of (valid, error_message)
        """
        return self._registry.validate_method_call(object_type, method_name, args, kwargs)
    
    def get_all_functions(self) -> List[VexFunctionSignature]:
        """Get all registered functions.
        
        Returns:
            List of all function signatures
        """
        return self._registry.get_all_functions()
    
    def get_function_names(self) -> Set[str]:
        """Get all registered function names.
        
        Returns:
            Set of function names
        """
        return {func.name for func in self.get_all_functions()}
    
    def get_categories(self) -> List[FunctionCategory]:
        """Get all available function categories.
        
        Returns:
            List of function categories
        """
        return list(FunctionCategory)
    
    def get_subcategories(self) -> List[SubCategory]:
        """Get all available function subcategories.
        
        Returns:
            List of function subcategories
        """
        return list(SubCategory)
    
    def get_simulation_categories(self) -> List[SimulationCategory]:
        """Get all available simulation categories.
        
        Returns:
            List of simulation categories
        """
        return list(SimulationCategory)

# Singleton instance
registry_api = RegistryAPI()
