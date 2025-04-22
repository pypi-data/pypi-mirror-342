"""Operator definitions for the AST."""

from enum import Enum, auto
from typing import Dict, Set, cast

class OperatorType(Enum):
    """Categories of operators."""
    BINARY = auto()
    UNARY = auto()
    COMPARISON = auto()
    LOGICAL = auto()

class Operator(Enum):
    """Enumeration of supported operators."""
    # Binary Arithmetic
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'
    POWER = '**'
    FLOOR_DIVIDE = '//'
    
    # Binary Bitwise
    BITWISE_AND = '&'
    BITWISE_OR = '|'
    BITWISE_XOR = '^'
    LEFT_SHIFT = '<<'
    RIGHT_SHIFT = '>>'
    
    # Binary Comparison
    EQUAL = '=='
    NOT_EQUAL = '!='
    LESS_THAN = '<'
    LESS_EQUAL = '<='
    GREATER_THAN = '>'
    GREATER_EQUAL = '>='
    
    # Binary Logical
    LOGICAL_AND = 'and'
    LOGICAL_OR = 'or'
    
    # Membership/Identity
    IN = 'in'
    NOT_IN = 'not in'
    IS = 'is'
    IS_NOT = 'is not'

    # Object access
    MEMBER_ACCESS = '.'  # Add this line
    
    # Unary Arithmetic
    UNARY_PLUS = '+ (unary)'
    UNARY_MINUS = '- (unary)'
    
    # Unary Bitwise
    BITWISE_NOT = '~'
    
    # Unary Logical
    LOGICAL_NOT = 'not'
    
    @classmethod
    def get_type(cls, op: 'Operator') -> OperatorType:
        """Get the type of an operator."""
        if op in UNARY_OPERATORS:
            return OperatorType.UNARY
        if op in COMPARISON_OPERATORS:
            return OperatorType.COMPARISON
        if op in LOGICAL_OPERATORS:
            return OperatorType.LOGICAL
        return OperatorType.BINARY

# Operator sets for validation
UNARY_OPERATORS: Set[Operator] = {
    Operator.UNARY_PLUS,
    Operator.UNARY_MINUS,
    Operator.BITWISE_NOT,
    Operator.LOGICAL_NOT
}

COMPARISON_OPERATORS: Set[Operator] = {
    Operator.EQUAL,
    Operator.NOT_EQUAL,
    Operator.LESS_THAN,
    Operator.LESS_EQUAL,
    Operator.GREATER_THAN,
    Operator.GREATER_EQUAL,
    Operator.IN,
    Operator.NOT_IN,
    Operator.IS,
    Operator.IS_NOT
}

LOGICAL_OPERATORS: Set[Operator] = {
    Operator.LOGICAL_AND,
    Operator.LOGICAL_OR
}

# Mappings for parser use
PYTHON_BINARY_OP_MAP: Dict[str, Operator] = {
    '+': Operator.ADD,
    '-': Operator.SUBTRACT,
    '*': Operator.MULTIPLY,
    '/': Operator.DIVIDE,
    '//': Operator.FLOOR_DIVIDE,
    '%': Operator.MODULO,
    '**': Operator.POWER,
    '<<': Operator.LEFT_SHIFT,
    '>>': Operator.RIGHT_SHIFT,
    '|': Operator.BITWISE_OR,
    '^': Operator.BITWISE_XOR,
    '&': Operator.BITWISE_AND,
    '@': Operator.MULTIPLY  # Matrix multiplication, maps to regular multiply for now
}

PYTHON_BINARY_OP_MAP['.'] = Operator.MEMBER_ACCESS

PYTHON_UNARY_OP_MAP: Dict[str, Operator] = {
    '+': Operator.UNARY_PLUS,
    '-': Operator.UNARY_MINUS,
    'not': Operator.LOGICAL_NOT,
    '~': Operator.BITWISE_NOT
}

PYTHON_COMP_OP_MAP: Dict[str, Operator] = {
    '==': Operator.EQUAL,
    '!=': Operator.NOT_EQUAL,
    '<': Operator.LESS_THAN,
    '<=': Operator.LESS_EQUAL,
    '>': Operator.GREATER_THAN,
    '>=': Operator.GREATER_EQUAL,
    'in': Operator.IN,
    'not in': Operator.NOT_IN,
    'is': Operator.IS,
    'is not': Operator.IS_NOT
}