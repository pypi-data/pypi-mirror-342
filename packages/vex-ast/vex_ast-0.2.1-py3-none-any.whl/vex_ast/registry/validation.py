from typing import Dict, List, Optional, Set, Tuple, Any, Union
from ..types.base import VexType
from ..types.type_checker import type_checker
from .registry import registry, VexFunctionRegistry
from .signature import VexFunctionSignature, VexFunctionParameter

class FunctionCallValidator:
    """Validates function calls against the registry"""
    
    def __init__(self, registry: VexFunctionRegistry = registry):
        self.registry = registry
    
    def validate_call(self, 
                    function_name: str, 
                    args: List[Any] = None,
                    kwargs: Dict[str, Any] = None,
                    language: str = "python") -> Tuple[bool, Optional[str]]:
        """Validate a function call"""
        args = args or []
        kwargs = kwargs or {}
        return self.registry.validate_call(function_name, args, kwargs, language)
    
    def validate_method_call(self,
                           object_type: Union[VexType, str],
                           method_name: str,
                           args: List[Any] = None,
                           kwargs: Dict[str, Any] = None) -> Tuple[bool, Optional[str]]:
        """Validate a method call on an object"""
        args = args or []
        kwargs = kwargs or {}
        return self.registry.validate_method_call(object_type, method_name, args, kwargs)
    
    def validate_ast_function_call(self, function_call_node: Any) -> Tuple[bool, Optional[str]]:
        """Validate a function call AST node"""
        # This would need to be implemented based on the actual AST node structure
        # For now, just a placeholder showing the interface
        function_name = function_call_node.function.name
        args = [arg.value for arg in function_call_node.args]
        kwargs = {kw.name: kw.value for kw in function_call_node.keywords}
        
        return self.validate_call(function_name, args, kwargs)

# Singleton instance
validator = FunctionCallValidator()