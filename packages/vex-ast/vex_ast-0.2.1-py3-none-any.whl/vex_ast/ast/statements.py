"""Statement nodes for the AST."""

from typing import Dict, List, Optional, Union, cast, Any

from .interfaces import IAstNode, IExpression, IStatement, IVisitor, T_VisitorResult, IAssignment
from .core import Statement, Expression
from .expressions import Identifier
from ..utils.source_location import SourceLocation

class ExpressionStatement(Statement):
    """An expression used as a statement."""
    
    _fields = ('expression',)
    
    def __init__(self, expression: IExpression, location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.expression = expression
        if isinstance(expression, Expression):
            expression.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        return [cast(IAstNode, self.expression)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_expressionstatement(self)
    
    def get_expression(self) -> IExpression:
        """Get the expression."""
        return self.expression

class Assignment(Statement, IAssignment):
    """An assignment statement (target = value)."""
    
    _fields = ('target', 'value')
    
    def __init__(self, target: IExpression, value: IExpression, 
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.target = target
        self.value = value
        if isinstance(target, Expression):
            target.set_parent(self)
        if isinstance(value, Expression):
            value.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        return [cast(IAstNode, self.target), cast(IAstNode, self.value)]
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_assignment(self)
    
    def get_target(self) -> IExpression:
        """Get the assignment target."""
        return self.target
    
    def get_value(self) -> IExpression:
        """Get the assigned value."""
        return self.value

class Argument(Statement):
    """A function argument in a definition."""
    
    _fields = ('name', 'annotation', 'default')
    
    def __init__(self, name: str, annotation: Optional[IExpression] = None,
                 default: Optional[IExpression] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.annotation = annotation
        self.default = default
        
        if isinstance(annotation, Expression):
            annotation.set_parent(self)
        if isinstance(default, Expression):
            default.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        result: List[IAstNode] = []
        if self.annotation:
            result.append(cast(IAstNode, self.annotation))
        if self.default:
            result.append(cast(IAstNode, self.default))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_argument(self)
    
    def get_name(self) -> str:
        """Get the argument name."""
        return self.name
    
    def get_annotation(self) -> Optional[IExpression]:
        """Get the type annotation, if any."""
        return self.annotation
    
    def get_default(self) -> Optional[IExpression]:
        """Get the default value, if any."""
        return self.default

class FunctionDefinition(Statement):
    """A function definition."""
    
    _fields = ('name', 'args', 'body', 'return_annotation')
    
    def __init__(self, name: str, args: List[Argument], body: List[IStatement],
                 return_annotation: Optional[IExpression] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.name = name
        self.args = args
        self.body = body
        self.return_annotation = return_annotation
        
        # Set parent references
        for arg in self.args:
            if isinstance(arg, Statement):
                arg.set_parent(self)
        
        for stmt in self.body:
            if isinstance(stmt, Statement):
                stmt.set_parent(self)
        
        if isinstance(return_annotation, Expression):
            return_annotation.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        result: List[IAstNode] = cast(List[IAstNode], self.args)
        result.extend(cast(List[IAstNode], self.body))
        if self.return_annotation:
            result.append(cast(IAstNode, self.return_annotation))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_functiondefinition(self)
    
    def get_name(self) -> str:
        """Get the function name."""
        return self.name
    
    def get_arguments(self) -> List[Argument]:
        """Get the function arguments."""
        return self.args
    
    def get_body(self) -> List[IStatement]:
        """Get the function body."""
        return self.body
    
    def get_return_annotation(self) -> Optional[IExpression]:
        """Get the return type annotation, if any."""
        return self.return_annotation
    
    def add_statement(self, statement: IStatement) -> None:
        """Add a statement to the function body."""
        self.body.append(statement)
        if isinstance(statement, Statement):
            statement.set_parent(self)

class IfStatement(Statement):
    """An if statement with optional else branch."""
    
    _fields = ('test', 'body', 'orelse')
    
    def __init__(self, test: IExpression, body: List[IStatement],
                 orelse: Optional[Union[List[IStatement], 'IfStatement']] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.test = test
        self.body = body
        self.orelse = orelse
        
        # Set parent references
        if isinstance(test, Expression):
            test.set_parent(self)
        
        for stmt in self.body:
            if isinstance(stmt, Statement):
                stmt.set_parent(self)
        
        if isinstance(self.orelse, list):
            for stmt in self.orelse:
                if isinstance(stmt, Statement):
                    stmt.set_parent(self)
        elif isinstance(self.orelse, Statement):
            self.orelse.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        result: List[IAstNode] = [cast(IAstNode, self.test)]
        result.extend(cast(List[IAstNode], self.body))
        if isinstance(self.orelse, list):
            result.extend(cast(List[IAstNode], self.orelse))
        elif self.orelse:
            result.append(cast(IAstNode, self.orelse))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_ifstatement(self)
    
    def get_test(self) -> IExpression:
        """Get the test condition."""
        return self.test
    
    def get_body(self) -> List[IStatement]:
        """Get the if body."""
        return self.body
    
    def get_else(self) -> Optional[Union[List[IStatement], 'IfStatement']]:
        """Get the else branch, if any."""
        return self.orelse
    
    def add_statement(self, statement: IStatement) -> None:
        """Add a statement to the if body."""
        self.body.append(statement)
        if isinstance(statement, Statement):
            statement.set_parent(self)

class WhileLoop(Statement):
    """A while loop."""
    
    _fields = ('test', 'body')
    
    def __init__(self, test: IExpression, body: List[IStatement],
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.test = test
        self.body = body
        
        # Set parent references
        if isinstance(test, Expression):
            test.set_parent(self)
        
        for stmt in self.body:
            if isinstance(stmt, Statement):
                stmt.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        result: List[IAstNode] = [cast(IAstNode, self.test)]
        result.extend(cast(List[IAstNode], self.body))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_whileloop(self)
    
    def get_test(self) -> IExpression:
        """Get the test condition."""
        return self.test
    
    def get_body(self) -> List[IStatement]:
        """Get the loop body."""
        return self.body
    
    def add_statement(self, statement: IStatement) -> None:
        """Add a statement to the loop body."""
        self.body.append(statement)
        if isinstance(statement, Statement):
            statement.set_parent(self)

class ForLoop(Statement):
    """A for loop (for target in iterable)."""
    
    _fields = ('target', 'iterable', 'body')
    
    def __init__(self, target: IExpression, iterable: IExpression, 
                 body: List[IStatement], location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.target = target
        self.iterable = iterable
        self.body = body
        
        # Set parent references
        if isinstance(target, Expression):
            target.set_parent(self)
        if isinstance(iterable, Expression):
            iterable.set_parent(self)
        
        for stmt in self.body:
            if isinstance(stmt, Statement):
                stmt.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        result: List[IAstNode] = [
            cast(IAstNode, self.target),
            cast(IAstNode, self.iterable)
        ]
        result.extend(cast(List[IAstNode], self.body))
        return result
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_forloop(self)
    
    def get_target(self) -> IExpression:
        """Get the loop target."""
        return self.target
    
    def get_iterable(self) -> IExpression:
        """Get the iterable expression."""
        return self.iterable
    
    def get_body(self) -> List[IStatement]:
        """Get the loop body."""
        return self.body
    
    def add_statement(self, statement: IStatement) -> None:
        """Add a statement to the loop body."""
        self.body.append(statement)
        if isinstance(statement, Statement):
            statement.set_parent(self)

class ReturnStatement(Statement):
    """A return statement."""
    
    _fields = ('value',)
    
    def __init__(self, value: Optional[IExpression] = None,
                 location: Optional[SourceLocation] = None):
        super().__init__(location)
        self.value = value
        if isinstance(value, Expression):
            value.set_parent(self)
    
    def get_children(self) -> List[IAstNode]:
        return [cast(IAstNode, self.value)] if self.value else []
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_returnstatement(self)
    
    def get_value(self) -> Optional[IExpression]:
        """Get the return value, if any."""
        return self.value

class BreakStatement(Statement):
    """A break statement."""
    
    _fields = ()
    
    def get_children(self) -> List[IAstNode]:
        return []
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_breakstatement(self)

class ContinueStatement(Statement):
    """A continue statement."""
    
    _fields = ()
    
    def get_children(self) -> List[IAstNode]:
        return []
    
    def accept(self, visitor: IVisitor[T_VisitorResult]) -> T_VisitorResult:
        return visitor.visit_continuestatement(self)
