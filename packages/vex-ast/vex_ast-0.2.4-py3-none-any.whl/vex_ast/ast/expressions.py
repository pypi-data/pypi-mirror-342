"""Expression nodes for the AST."""

from typing import Dict, List, Optional, Union, cast, Any

from .interfaces import IAstNode, IExpression, IVisitor, T_VisitorResult, IIdentifier, IFunctionCall, IConditionalExpression
from .core import Expression
from .operators import Operator
from ..utils.source_location import SourceLocation

class Identifier(Expression, IIdentifier):
    """An identifier (variable name, function name, etc.)."""
    
    _fields = ('name',)
    
    def __init__(self, name: str, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
    
    def get_children(self) -> List[IAstNode]:
        """Identifiers have no children."""
        return []
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_identifier(self)
    
    def get_name(self) -> str:
        """Get the identifier name."""
        return self.name

class VariableReference(Expression):
    """A reference to a variable."""
    
    _fields = ('identifier',)
    
    def __init__(self, identifier: Identifier, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.identifier = identifier
        if isinstance(identifier, Expression):
            identifier.set_parent(self)
    
    @property
    def name(self) -> str:
        """Convenience property to get the variable name."""
        return self.identifier.name
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [self.identifier]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_variablereference(self)
    
    def get_identifier(self) -> IIdentifier:
        """Get the identifier being referenced."""
        return self.identifier

class AttributeAccess(Expression):
    """An attribute access expression (e.g., object.attribute)."""
    
    _fields = ('object', 'attribute')
    
    def __init__(self, object_expr: IExpression, attribute: str, 
                location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.object = object_expr
        self.attribute = attribute
        if isinstance(object_expr, Expression):
            object_expr.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [cast(IAstNode, self.object)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_attributeaccess(self)
    
    def get_object(self) -> IExpression:
        """Get the object expression."""
        return self.object
    
    def get_attribute_name(self) -> str:
        """Get the attribute name."""
        return self.attribute

class BinaryOperation(Expression):
    """A binary operation (e.g., a + b)."""
    
    _fields = ('left', 'op', 'right')
    
    def __init__(self, left: IExpression, op: Operator, right: IExpression, 
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.left = left
        self.op = op
        self.right = right
        if isinstance(left, Expression):
            left.set_parent(self)
        if isinstance(right, Expression):
            right.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [cast(IAstNode, self.left), cast(IAstNode, self.right)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_binaryoperation(self)
    
    def get_left(self) -> IExpression:
        """Get the left operand."""
        return self.left
    
    def get_right(self) -> IExpression:
        """Get the right operand."""
        return self.right
    
    def get_operator(self) -> Operator:
        """Get the operator."""
        return self.op

class UnaryOperation(Expression):
    """A unary operation (e.g., -a, not b)."""
    
    _fields = ('op', 'operand')
    
    def __init__(self, op: Operator, operand: IExpression, 
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.op = op
        self.operand = operand
        if isinstance(operand, Expression):
            operand.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [cast(IAstNode, self.operand)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_unaryoperation(self)
    
    def get_operand(self) -> IExpression:
        """Get the operand."""
        return self.operand
    
    def get_operator(self) -> Operator:
        """Get the operator."""
        return self.op

class KeywordArgument(Expression):
    """A keyword argument in a function call (name=value)."""
    
    _fields = ('name', 'value')
    
    def __init__(self, name: str, value: IExpression, 
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.value = value
        if isinstance(value, Expression):
            value.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [cast(IAstNode, self.value)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_keywordargument(self)
    
    def get_name(self) -> str:
        """Get the keyword name."""
        return self.name
    
    def get_value(self) -> IExpression:
        """Get the keyword value."""
        return self.value

class ConditionalExpression(Expression, IConditionalExpression):
    """A conditional expression (ternary operator, e.g., a if condition else b)."""
    
    _fields = ('condition', 'true_expr', 'false_expr')
    
    def __init__(self, condition: IExpression, true_expr: IExpression, false_expr: IExpression,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
        
        # Set parent references
        if isinstance(condition, Expression):
            condition.set_parent(self)
        if isinstance(true_expr, Expression):
            true_expr.set_parent(self)
        if isinstance(false_expr, Expression):
            false_expr.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        return [
            cast(IAstNode, self.condition),
            cast(IAstNode, self.true_expr),
            cast(IAstNode, self.false_expr)
        ]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_conditionalexpression(self)
    
    def get_condition(self) -> IExpression:
        """Get the condition expression."""
        return self.condition
    
    def get_true_expression(self) -> IExpression:
        """Get the expression to evaluate if condition is true."""
        return self.true_expr
    
    def get_false_expression(self) -> IExpression:
        """Get the expression to evaluate if condition is false."""
        return self.false_expr

class FunctionCall(Expression, IFunctionCall):
    """A function call."""
    
    _fields = ('function', 'args', 'keywords')
    
    def __init__(self, function: IExpression, args: List[IExpression],
                 keywords: List[KeywordArgument] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.function = function
        self.args = args or []
        self.keywords = keywords or []
        
        # Set parent references
        if isinstance(function, Expression):
            function.set_parent(self)
        
        for arg in self.args:
            if isinstance(arg, Expression):
                arg.set_parent(self)
        
        for kw in self.keywords:
            if isinstance(kw, Expression):
                kw.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        """Get child nodes."""
        result: List[IAstNode] = [cast(IAstNode, self.function)]
        result.extend(cast(List[IAstNode], self.args))
        result.extend(cast(List[IAstNode], self.keywords))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_functioncall(self)
    
    def get_function_expr(self) -> IExpression:
        """Get the function expression."""
        return self.function
    
    def get_arguments(self) -> List[IExpression]:
        """Get the positional arguments."""
        return self.args
    
    def get_keyword_arguments(self) -> Dict[str, IExpression]:
        """Get the keyword arguments as a dictionary."""
        return {kw.name: kw.value for kw in self.keywords}
    
    def add_argument(self, arg: IExpression) -> None:
        """Add a positional argument."""
        self.args.append(arg)
        if isinstance(arg, Expression):
            arg.set_parent(self)
    
    def add_keyword_argument(self, name: str, value: IExpression) -> None:
        """Add a keyword argument."""
        kw = KeywordArgument(name, value)
        self.keywords.append(kw)
        kw.set_parent(self)
