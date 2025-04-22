"""Node factory for creating AST nodes (Factory Pattern)."""

from typing import Any, Dict, Optional, Type, Union, cast, List

from ..ast.core import Expression, Program, Statement
from ..ast.expressions import (
    AttributeAccess, BinaryOperation, FunctionCall, Identifier, KeywordArgument, 
    UnaryOperation, VariableReference
)
from ..ast.literals import (
    BooleanLiteral, NoneLiteral, NumberLiteral, StringLiteral
)
from ..ast.operators import Operator
from ..ast.statements import (
    Assignment, BreakStatement, ContinueStatement, ExpressionStatement,
    ForLoop, FunctionDefinition, IfStatement, ReturnStatement, WhileLoop, Argument
)
from ..ast.vex_nodes import (
    DisplayOutput, MotorControl, SensorReading, TimingControl, VexAPICall
)
from ..utils.errors import ErrorHandler
from ..utils.source_location import SourceLocation

class NodeFactory:
    """Factory for creating AST nodes."""
    
    def __init__(self, error_handler: Optional[ErrorHandler] = None):
        """Initialize with an optional error handler."""
        self.error_handler = error_handler
    
    # --- Literals ---
    
    def create_number_literal(self, value: Union[int, float], 
                              location: Optional[SourceLocation] = None) -> NumberLiteral:
        """Create a number literal node."""
        return NumberLiteral(value, location)
    
    def create_string_literal(self, value: str,
                              location: Optional[SourceLocation] = None) -> StringLiteral:
        """Create a string literal node."""
        return StringLiteral(value, location)
    
    def create_boolean_literal(self, value: bool,
                               location: Optional[SourceLocation] = None) -> BooleanLiteral:
        """Create a boolean literal node."""
        return BooleanLiteral(value, location)
    
    def create_none_literal(self, 
                            location: Optional[SourceLocation] = None) -> NoneLiteral:
        """Create a None literal node."""
        return NoneLiteral(location)
    
    # --- Expressions ---
    
    def create_identifier(self, name: str,
                          location: Optional[SourceLocation] = None) -> Identifier:
        """Create an identifier node."""
        return Identifier(name, location)
    
    def create_variable_reference(self, identifier: Identifier,
                                  location: Optional[SourceLocation] = None) -> VariableReference:
        """Create a variable reference node."""
        return VariableReference(identifier, location)
    
    def create_attribute_access(self, object_expr: Expression, attribute: str,
                                location: Optional[SourceLocation] = None) -> AttributeAccess:
        """Create an attribute access node."""
        return AttributeAccess(object_expr, attribute, location)
    
    def create_binary_operation(self, left: Expression, op: Operator, right: Expression,
                                location: Optional[SourceLocation] = None) -> BinaryOperation:
        """Create a binary operation node."""
        return BinaryOperation(left, op, right, location)
    
    def create_unary_operation(self, op: Operator, operand: Expression,
                               location: Optional[SourceLocation] = None) -> UnaryOperation:
        """Create a unary operation node."""
        return UnaryOperation(op, operand, location)
    
    def create_function_call(self, function: Expression, args: List[Expression] = None,
                             keywords: List[KeywordArgument] = None,
                             location: Optional[SourceLocation] = None) -> FunctionCall:
        """Create a function call node."""
        return FunctionCall(function, args or [], keywords or [], location)
    
    def create_keyword_argument(self, name: str, value: Expression,
                                location: Optional[SourceLocation] = None) -> KeywordArgument:
        """Create a keyword argument node."""
        return KeywordArgument(name, value, location)
    
    # --- Statements ---
    
    def create_expression_statement(self, expression: Expression,
                                   location: Optional[SourceLocation] = None) -> ExpressionStatement:
        """Create an expression statement node."""
        return ExpressionStatement(expression, location)
    
    def create_assignment(self, target: Expression, value: Expression,
                          location: Optional[SourceLocation] = None) -> Assignment:
        """Create an assignment statement node."""
        return Assignment(target, value, location)
    
    def create_if_statement(self, test: Expression, body: List[Statement],
                           orelse: Optional[Union[List[Statement], IfStatement]] = None,
                           location: Optional[SourceLocation] = None) -> IfStatement:
        """Create an if statement node."""
        return IfStatement(test, body, orelse, location)
    
    def create_while_loop(self, test: Expression, body: List[Statement],
                         location: Optional[SourceLocation] = None) -> WhileLoop:
        """Create a while loop node."""
        return WhileLoop(test, body, location)
    
    def create_for_loop(self, target: Expression, iterable: Expression, 
                       body: List[Statement],
                       location: Optional[SourceLocation] = None) -> ForLoop:
        """Create a for loop node."""
        return ForLoop(target, iterable, body, location)
    
    def create_function_definition(self, name: str, args: List[Argument], body: List[Statement],
                                  return_annotation: Optional[Expression] = None,
                                  location: Optional[SourceLocation] = None) -> FunctionDefinition:
        """Create a function definition node."""
        return FunctionDefinition(name, args, body, return_annotation, location)
    
    def create_return_statement(self, value: Optional[Expression] = None,
                               location: Optional[SourceLocation] = None) -> ReturnStatement:
        """Create a return statement node."""
        return ReturnStatement(value, location)
    
    def create_break_statement(self, 
                              location: Optional[SourceLocation] = None) -> BreakStatement:
        """Create a break statement node."""
        return BreakStatement(location)
    
    def create_continue_statement(self,
                                 location: Optional[SourceLocation] = None) -> ContinueStatement:
        """Create a continue statement node."""
        return ContinueStatement(location)
    
    # --- VEX-specific Nodes ---
    
    def create_vex_api_call(self, function: Expression, args: List[Expression],
                           keywords: List[KeywordArgument] = None,
                           location: Optional[SourceLocation] = None) -> VexAPICall:
        """Create a VEX API call node."""
        return VexAPICall(function, args, keywords or [], location)
    
    def create_motor_control(self, function: Expression, args: List[Expression],
                            keywords: List[KeywordArgument] = None,
                            location: Optional[SourceLocation] = None) -> MotorControl:
        """Create a motor control node."""
        return MotorControl(function, args, keywords or [], location)
    
    def create_sensor_reading(self, function: Expression, args: List[Expression],
                             keywords: List[KeywordArgument] = None,
                             location: Optional[SourceLocation] = None) -> SensorReading:
        """Create a sensor reading node."""
        return SensorReading(function, args, keywords or [], location)
    
    def create_timing_control(self, function: Expression, args: List[Expression],
                             keywords: List[KeywordArgument] = None,
                             location: Optional[SourceLocation] = None) -> TimingControl:
        """Create a timing control node."""
        return TimingControl(function, args, keywords or [], location)
    
    def create_display_output(self, function: Expression, args: List[Expression],
                             keywords: List[KeywordArgument] = None,
                             location: Optional[SourceLocation] = None) -> DisplayOutput:
        """Create a display output node."""
        return DisplayOutput(function, args, keywords or [], location)
    
    def create_program(self, body: List[Statement],
                      location: Optional[SourceLocation] = None) -> Program:
        """Create a program node."""
        return Program(body, location)

# Global factory instance for simple use cases
default_factory = NodeFactory()