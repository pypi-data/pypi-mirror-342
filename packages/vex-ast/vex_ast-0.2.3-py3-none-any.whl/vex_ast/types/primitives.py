from typing import Optional, Union, List, Set, Dict, Any
from .base import VexType, type_registry

class PrimitiveType(VexType):
    """Base class for primitive types like int, float, string, etc."""
    
    def __init__(self, name: str):
        self._name = name
        type_registry.register_type(self)
    
    @property
    def name(self) -> str:
        return self._name
    
    def __str__(self) -> str:
        return self._name

class NumericType(PrimitiveType):
    """Base class for numeric types"""
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Numeric types are compatible with other numeric types"""
        return isinstance(other, NumericType)

class IntegerType(NumericType):
    """Integer type"""
    
    def __init__(self):
        super().__init__("int")
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Integers are compatible with numeric types"""
        return isinstance(other, NumericType)

class FloatType(NumericType):
    """Float type"""
    
    def __init__(self):
        super().__init__("float")
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Floats are compatible with numeric types"""
        return isinstance(other, NumericType)

class BooleanType(PrimitiveType):
    """Boolean type"""
    
    def __init__(self):
        super().__init__("bool")
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Booleans are only compatible with booleans"""
        return isinstance(other, BooleanType)

class StringType(PrimitiveType):
    """String type"""
    
    def __init__(self):
        super().__init__("string")
    
    def is_compatible_with(self, other: VexType) -> bool:
        """Strings are only compatible with strings"""
        return isinstance(other, StringType)

# Singleton instances
INT = IntegerType()
FLOAT = FloatType()
BOOL = BooleanType()
STRING = StringType()