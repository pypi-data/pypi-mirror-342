"""Source location tracking for AST nodes."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class SourceLocation:
    """Represents a location in source code."""
    
    # Start position
    line: int
    column: int
    
    # End position (optional)
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    
    # Source file
    filename: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize the location data."""
        # Ensure end line is at least start line if not specified
        if self.end_line is None:
            self.end_line = self.line
    
    def __str__(self) -> str:
        """Format the location for display."""
        file_prefix = f"{self.filename}:" if self.filename else ""
        
        # Just a point or single line span
        if self.end_line == self.line:
            if self.end_column is None or self.end_column == self.column:
                return f"{file_prefix}L{self.line}:{self.column}"
            return f"{file_prefix}L{self.line}:{self.column}-{self.end_column}"
        
        # Multi-line span
        end_col = f":{self.end_column}" if self.end_column is not None else ""
        return f"{file_prefix}L{self.line}:{self.column}-L{self.end_line}{end_col}"