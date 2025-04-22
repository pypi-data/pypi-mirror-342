AST Visitors (vex_ast.visitors)

This directory provides implementations of the Visitor design pattern for traversing and operating on the VEX Abstract Syntax Tree (AST).

Purpose

Visitors allow you to perform operations on the AST without modifying the AST node classes themselves. They provide a clean and extensible way to implement various forms of analysis, transformation, or code generation based on the AST structure.

Core Concepts

Visitor Pattern: The core idea is double dispatch. You call visitor.visit(node), which in turn calls node.accept(visitor). The node's accept method then calls the specific visit_NodeType(node) method on the visitor corresponding to its own type.

Base Visitor (base.py):

AstVisitor[T_VisitorResult]: An abstract generic base class for all visitors. It defines the main visit entry point and provides default visit_NodeType methods that typically delegate to a generic_visit method. Subclasses must implement generic_visit and can override specific visit_NodeType methods for custom behavior.

Traversal: The generic_visit method in concrete visitors often iterates through the node's children (obtained via node.get_children()) and calls self.visit(child) recursively to traverse the tree.

Provided Visitors

Printer (printer.py):

PrintVisitor: Traverses the AST and generates a formatted, indented string representation of the tree structure, including node types, attributes, and source locations (if available). Useful for debugging and understanding the AST structure.

Analyzers (analyzer.py):

NodeCounter: Traverses the AST and counts the total number of nodes, optionally keeping track of counts per node type.

VariableCollector: Traverses the AST and collects the names of all variables referenced (VariableReference nodes).

Usage

Instantiate a Visitor: Create an instance of the desired visitor class (e.g., printer = PrintVisitor()).

Parse Code: Obtain the root node (Program object) of the AST using vex_ast.parse_string or vex_ast.parse_file.

Start Visitation: Call the visitor's visit method with the root node (e.g., result = printer.visit(ast_root)).

Process Result: The visit method will return a result whose type depends on the specific visitor (T_VisitorResult). For PrintVisitor, it's a string; for NodeCounter, an integer; for VariableCollector, a set of strings.

Extensibility

You can create custom visitors to perform specific tasks (e.g., type checking, code optimization, simulation execution) by:

Creating a new class that inherits from AstVisitor[YourResultType].

Implementing the generic_visit method to define default behavior and traversal logic.

Overriding specific visit_NodeType methods for nodes where specialized logic is required.
