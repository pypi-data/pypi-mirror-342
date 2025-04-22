from typing import Optional, Any, List, Dict, Union, Tuple
from .base import VexType, ANY
from .primitives import INT, FLOAT, BOOL, STRING

class TypeChecker:
    """Utility for checking type compatibility"""
    
    def is_compatible(self, value_type: VexType, expected_type: VexType) -> bool:
        """Check if value_type is compatible with expected_type"""
        # Any type is compatible with anything
        if expected_type == ANY:
            return True
            
        return value_type.is_compatible_with(expected_type)
    
    def get_python_type(self, value: Any) -> Optional[VexType]:
        """Convert a Python value to a VEX type"""
        if value is None:
            return None
        if isinstance(value, bool):
            return BOOL
        if isinstance(value, int):
            return INT
        if isinstance(value, float):
            return FLOAT
        if isinstance(value, str):
            return STRING
        # Complex objects would need additional mapping logic
        return None

# Singleton instance
type_checker = TypeChecker()