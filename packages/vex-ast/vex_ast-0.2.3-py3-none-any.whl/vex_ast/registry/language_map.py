from typing import Dict, Set, List, Optional, Tuple

class LanguageMapper:
    """Utility for mapping between Python and C++ function names"""
    
    def __init__(self):
        self.python_to_cpp: Dict[str, str] = {}
        self.cpp_to_python: Dict[str, str] = {}
        
        # Common pattern transformations
        # Python: snake_case, C++: camelCase or PascalCase
        self.python_patterns = {
            "set_": "set",
            "get_": "get",
            "is_": "is",
            "has_": "has",
        }
    
    def register_mapping(self, python_name: str, cpp_name: str) -> None:
        """Register a mapping between Python and C++ function names"""
        self.python_to_cpp[python_name] = cpp_name
        self.cpp_to_python[cpp_name] = python_name
    
    def get_cpp_name(self, python_name: str) -> Optional[str]:
        """Get the C++ name for a Python function name"""
        # Direct lookup
        if python_name in self.python_to_cpp:
            return self.python_to_cpp[python_name]
        
        # Try pattern matching
        for py_pattern, cpp_pattern in self.python_patterns.items():
            if python_name.startswith(py_pattern):
                # Convert snake_case to camelCase
                rest = python_name[len(py_pattern):]
                parts = rest.split('_')
                camel_case = parts[0] + ''.join(part.capitalize() for part in parts[1:])
                return cpp_pattern + camel_case.capitalize()
        
        # Default: convert snake_case to camelCase
        parts = python_name.split('_')
        return parts[0] + ''.join(part.capitalize() for part in parts[1:])
    
    def get_python_name(self, cpp_name: str) -> Optional[str]:
        """Get the Python name for a C++ function name"""
        # Direct lookup
        if cpp_name in self.cpp_to_python:
            return self.cpp_to_python[cpp_name]
        
        # Try to convert camelCase to snake_case
        result = ''
        for char in cpp_name:
            if char.isupper() and result:
                result += '_'
            result += char.lower()
        return result

# Singleton instance
language_mapper = LanguageMapper()

# Register common VEX function mappings
common_mappings = {
    # Motor functions
    "spin": "spin",
    "stop": "stop",
    "set_velocity": "setVelocity",
    "set_stopping": "setStopping",
    
    # Drivetrain functions
    "drive": "drive",
    "turn": "turn",
    "drive_for": "driveFor",
    "turn_for": "turnFor",
    
    # Add more mappings as needed
}

for py_name, cpp_name in common_mappings.items():
    language_mapper.register_mapping(py_name, cpp_name)