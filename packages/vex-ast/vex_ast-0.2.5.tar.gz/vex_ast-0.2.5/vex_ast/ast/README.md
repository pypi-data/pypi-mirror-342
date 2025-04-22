AST Node Definitions (vex_ast.ast)

This directory defines the structure and types of nodes used in the Abstract Syntax Tree (AST) representation of VEX V5 Python code.

Purpose

The AST provides a structured, hierarchical representation of the source code, abstracting away the specific syntax details. This structure is the foundation for analysis, transformation, and interpretation of the code.

Core Concepts

Interfaces (interfaces.py): Defines the fundamental protocols (IAstNode, IExpression, IStatement, ILiteral, IVisitor) that all nodes and visitors adhere to. This ensures a consistent structure.

Base Classes (core.py): Provides abstract base classes (AstNode, Expression, Statement) that implement common functionality like location tracking and the basic accept method for the Visitor pattern. Program is the root node type.

Visitor Pattern: Each node implements an accept(visitor) method, allowing external IVisitor objects to operate on the AST without modifying the node classes themselves.

Child Nodes: Each node provides a get_children() method to facilitate traversal of the tree.

Source Location: Nodes can store optional SourceLocation information (from vex_ast.utils) linking them back to the original code.

Node Categories

The AST nodes are organized into logical categories:

Expressions (expressions.py): Represent code constructs that evaluate to a value.

Identifier: Variable names, function names.

VariableReference: Usage of a variable.

AttributeAccess: Accessing attributes (e.g., motor.spin).

BinaryOperation: Operations like +, -, *, /, ==, and, or.

UnaryOperation: Operations like - (negation), not.

FunctionCall: Calling functions or methods.

KeywordArgument: Named arguments in function calls (e.g., speed=50).

Literals (literals.py): Represent constant values.

NumberLiteral: Integers and floats.

StringLiteral: Text strings.

BooleanLiteral: True or False.

NoneLiteral: The None value.

Statements (statements.py): Represent actions or control flow constructs.

ExpressionStatement: An expression used on its own line (e.g., a function call).

Assignment: Assigning a value to a variable (=).

IfStatement: Conditional execution (if/elif/else).

WhileLoop: Looping based on a condition.

ForLoop: Iterating over a sequence.

FunctionDefinition: Defining a function (def).

Argument: Parameters in a function definition.

ReturnStatement: Returning a value from a function.

BreakStatement, ContinueStatement: Loop control.

Operators (operators.py): Defines Operator enums used within BinaryOperation and UnaryOperation nodes. Includes mappings from Python operators.

VEX-Specific Nodes (vex_nodes.py): Subclasses of FunctionCall tailored to represent common VEX API patterns.

VexAPICall: Base class for VEX calls.

MotorControl: Calls related to motors (e.g., motor.spin).

SensorReading: Calls related to sensors (e.g., sensor.value).

TimingControl: Calls like wait.

DisplayOutput: Calls related to screen output (e.g., brain.screen.print).

Usage

These node classes are typically instantiated by the parser (vex_ast.parser) during the code parsing process. Visitors (vex_ast.visitors) then interact with these node objects to perform tasks.
