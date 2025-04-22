"""Abstract Syntax Tree (AST) package for VEX code."""

# Core AST classes
from .interfaces import (
    IAstNode, IExpression, IStatement, ILiteral, IIdentifier, IFunctionCall, IAssignment,
    IVisitor, T_VisitorResult, AstNode
)
from .core import Expression, Statement, Program
from .expressions import (
    Identifier, VariableReference, AttributeAccess,
    BinaryOperation, UnaryOperation, FunctionCall, KeywordArgument
)
from .statements import (
    ExpressionStatement, Assignment, Argument, FunctionDefinition,
    IfStatement, WhileLoop, ForLoop, ReturnStatement,
    BreakStatement, ContinueStatement
)
from .literals import (
    Literal, NumberLiteral, StringLiteral, BooleanLiteral, NoneLiteral
)
from .operators import Operator
from .vex_nodes import (
    VexAPICallType, VexAPICall, MotorControl, SensorReading,
    TimingControl, DisplayOutput, create_vex_api_call,
    create_vex_api_call_from_interface
)
from .validators import validate_vex_functions, VexFunctionValidator
from .navigator import AstNavigator

# Expose the navigator as a factory function
def create_navigator(root: IAstNode) -> AstNavigator:
    """Create an AST navigator for the given root node.
    
    Args:
        root: The root node of the AST
        
    Returns:
        An AST navigator for traversing and querying the AST
    """
    return AstNavigator(root)

__all__ = [
    # Interfaces
    'IAstNode', 'IExpression', 'IStatement', 'ILiteral', 'IIdentifier', 
    'IFunctionCall', 'IAssignment', 'IVisitor', 'T_VisitorResult', 'AstNode',
    
    # Core
    'Expression', 'Statement', 'Program',
    
    # Expressions
    'Identifier', 'VariableReference', 'AttributeAccess',
    'BinaryOperation', 'UnaryOperation', 'FunctionCall', 'KeywordArgument',
    
    # Statements
    'ExpressionStatement', 'Assignment', 'Argument', 'FunctionDefinition',
    'IfStatement', 'WhileLoop', 'ForLoop', 'ReturnStatement',
    'BreakStatement', 'ContinueStatement',
    
    # Literals
    'Literal', 'NumberLiteral', 'StringLiteral', 'BooleanLiteral', 'NoneLiteral',
    
    # Operators
    'Operator',
    
    # VEX-specific
    'VexAPICallType', 'VexAPICall', 'MotorControl', 'SensorReading',
    'TimingControl', 'DisplayOutput', 'create_vex_api_call',
    'create_vex_api_call_from_interface',
    
    # Validators
    'validate_vex_functions', 'VexFunctionValidator',
    
    # Navigator
    'AstNavigator', 'create_navigator',
]
