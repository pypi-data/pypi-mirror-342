"""Registry package for VEX AST functions and types."""

from .registry import registry, VexFunctionRegistry
from .signature import (
    VexFunctionSignature, 
    VexFunctionParameter, 
    ParameterMode,
    SimulationCategory
)
from .categories import (
    FunctionCategory, 
    SubCategory,
    categorizer
)
from .language_map import language_mapper
from .validation import validator
from .simulation_behavior import SimulationBehavior
from .api import registry_api, RegistryAPI

# Initialize registry with default values
def initialize():
    """Initialize the registry with all VEX functions"""
    from .functions.initialize import initialize_registry
    initialize_registry()

__all__ = [
    # Legacy direct access (deprecated)
    'registry',
    'VexFunctionRegistry',
    
    # Preferred API access
    'registry_api',
    'RegistryAPI',
    
    # Common types and enums
    'VexFunctionSignature',
    'VexFunctionParameter',
    'ParameterMode',
    'SimulationCategory',
    'SimulationBehavior',
    'FunctionCategory',
    'SubCategory',
    
    # Utility objects
    'categorizer',
    'language_mapper',
    'validator',
    
    # Functions
    'initialize'
]
