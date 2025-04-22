"""Error handling framework for the VEX AST."""

import logging
from enum import Enum, auto
from typing import List, Optional, Callable, Protocol, Any, TypeVar, cast

from .source_location import SourceLocation

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Types of errors that can occur during AST processing."""
    LEXER_ERROR = auto()
    PARSER_ERROR = auto()
    TYPE_ERROR = auto()
    SEMANTIC_ERROR = auto()
    INTERNAL_ERROR = auto()

class Error:
    """Represents a single error detected during processing."""
    
    def __init__(self, 
                 error_type: ErrorType,
                 message: str,
                 location: Optional[SourceLocation] = None,
                 suggestion: Optional[str] = None):
        self.error_type = error_type
        self.message = message
        self.location = location
        self.suggestion = suggestion
    
    def __str__(self) -> str:
        """Format the error for display."""
        loc_str = f" at {self.location}" if self.location else ""
        sugg_str = f"\n  Suggestion: {self.suggestion}" if self.suggestion else ""
        return f"[{self.error_type.name}]{loc_str}: {self.message}{sugg_str}"

# Error handler callback protocol
T_Error = TypeVar('T_Error', bound=Error)

class ErrorObserver(Protocol[T_Error]):
    """Protocol for objects that can observe errors."""
    
    def on_error(self, error: T_Error) -> None:
        """Handle an error notification."""
        ...

class ErrorHandler:
    """Manages error collection and notification."""
    
    def __init__(self, raise_on_error: bool = True):
        self._errors: List[Error] = []
        self._raise_on_error = raise_on_error
        self._observers: List[ErrorObserver] = []
    
    def add_error(self,
                  error_type: ErrorType,
                  message: str,
                  location: Optional[SourceLocation] = None,
                  suggestion: Optional[str] = None) -> None:
        """Add an error to the collection."""
        error = Error(error_type, message, location, suggestion)
        self._errors.append(error)
        logger.error(str(error))
        
        # Notify observers
        for observer in self._observers:
            try:
                observer.on_error(error)
            except Exception as e:
                logger.exception(f"Error observer failed: {e}")
        
        if self._raise_on_error:
            if error_type == ErrorType.PARSER_ERROR:
                raise VexSyntaxError(message, location)
            else:
                raise VexAstError(str(error))
    
    def get_errors(self) -> List[Error]:
        """Get a copy of all collected errors."""
        return self._errors.copy()
    
    def has_errors(self) -> bool:
        """Check if any errors have been collected."""
        return bool(self._errors)
    
    def clear_errors(self) -> None:
        """Clear all collected errors."""
        self._errors.clear()
    
    def add_observer(self, observer: ErrorObserver) -> None:
        """Add an observer to be notified of errors."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: ErrorObserver) -> None:
        """Remove an error observer."""
        if observer in self._observers:
            self._observers.remove(observer)

class VexAstError(Exception):
    """Base exception class for VEX AST errors."""
    pass

class VexSyntaxError(VexAstError):
    """Exception raised for syntax errors during parsing."""
    
    def __init__(self, message: str, location: Optional[SourceLocation] = None):
        self.location = location
        super().__init__(message)
