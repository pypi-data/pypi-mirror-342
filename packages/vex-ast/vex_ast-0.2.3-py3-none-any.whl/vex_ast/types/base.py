from abc import ABC, abstractmethod
from typing import Any, Optional, Union, List, Type, Set, TypeVar, Generic

class VexType(ABC):
    """Base abstract class for all VEX types"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the canonical name of this type"""
        pass
    
    @abstractmethod
    def is_compatible_with(self, other: 'VexType') -> bool:
        """Check if this type is compatible with another type"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """String representation of the type"""
        pass
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, VexType):
            return False
        return self.name == other.name

class VoidType(VexType):
    """Represents the void type (no return value)"""
    
    @property
    def name(self) -> str:
        return "void"
    
    def is_compatible_with(self, other: VexType) -> bool:
        return isinstance(other, VoidType)
    
    def __str__(self) -> str:
        return "void"

class AnyType(VexType):
    """Represents any type (for generic functions)"""
    
    @property
    def name(self) -> str:
        return "any"
    
    def is_compatible_with(self, other: VexType) -> bool:
        return True  # Any type is compatible with all types
    
    def __str__(self) -> str:
        return "any"

class TypeRegistry:
    """Global registry of types to ensure type uniqueness"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypeRegistry, cls).__new__(cls)
            cls._instance._types = {}
        return cls._instance
    
    def register_type(self, type_: VexType) -> None:
        """Register a type in the registry"""
        self._types[type_.name] = type_
    
    def get_type(self, name: str) -> Optional[VexType]:
        """Get a type by name"""
        return self._types.get(name)
    
    def get_all_types(self) -> List[VexType]:
        """Get all registered types"""
        return list(self._types.values())

# Singleton instances
VOID = VoidType()
ANY = AnyType()

# Global registry
type_registry = TypeRegistry()
type_registry.register_type(VOID)
type_registry.register_type(ANY)