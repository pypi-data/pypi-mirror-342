"""Parser interfaces and protocols."""

from abc import ABC, abstractmethod
from typing import Protocol, Optional

from ..ast.core import Program
from ..utils.errors import ErrorHandler

class IParser(Protocol):
    """Protocol for parser implementations."""
    
    def parse(self) -> Program:
        """Parse the input and return an AST."""
        ...
    
    @property
    def error_handler(self) -> Optional[ErrorHandler]:
        """Get the parser's error handler."""
        ...

class BaseParser(ABC):
    """Abstract base class for parsers."""
    
    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        self._error_handler = error_handler or ErrorHandler()
    
    @property
    def error_handler(self) -> ErrorHandler:
        """Get the parser's error handler."""
        return self._error_handler
    
    @abstractmethod
    def parse(self) -> Program:
        """Parse the input and return an AST."""
        pass