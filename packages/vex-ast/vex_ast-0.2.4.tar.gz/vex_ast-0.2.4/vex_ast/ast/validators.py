"""AST validators that use the function registry."""

from typing import List, Dict, Set, Optional, Tuple
from .core import Program
from .expressions import FunctionCall, AttributeAccess, Identifier
from .vex_nodes import VexAPICall
from ..visitors.base import AstVisitor
from ..registry.api import registry_api

class VexFunctionValidator(AstVisitor[List[Tuple[VexAPICall, str]]]):
    """Validates VEX function calls in the AST"""
    
    def __init__(self):
        self.errors: List[Tuple[VexAPICall, str]] = []
    
    def generic_visit(self, node):
        """Visit children of non-VEX-specific nodes"""
        for child in node.get_children():
            self.visit(child)
        return self.errors
    
    def visit_vexapicall(self, node: VexAPICall):
        """Validate a VEX API call"""
        valid, error = node.validate()
        if not valid and error:
            self.errors.append((node, error))
        
        # Still visit children for nested calls
        for child in node.get_children():
            self.visit(child)
        
        return self.errors
    
    visit_program = generic_visit
    visit_expression = generic_visit
    visit_statement = generic_visit
    visit_identifier = generic_visit
    visit_variablereference = generic_visit
    visit_attributeaccess = generic_visit
    visit_binaryoperation = generic_visit
    visit_unaryoperation = generic_visit
    visit_keywordargument = generic_visit
    visit_numberliteral = generic_visit
    visit_stringliteral = generic_visit
    visit_booleanliteral = generic_visit
    visit_noneliteral = generic_visit
    visit_expressionstatement = generic_visit
    visit_assignment = generic_visit
    visit_ifstatement = generic_visit
    visit_whileloop = generic_visit
    visit_forloop = generic_visit
    visit_functiondefinition = generic_visit
    visit_argument = generic_visit
    visit_returnstatement = generic_visit
    visit_breakstatement = generic_visit
    visit_continuestatement = generic_visit
    visit_motorcontrol = visit_vexapicall
    visit_sensorreading = visit_vexapicall
    visit_timingcontrol = visit_vexapicall
    visit_displayoutput = visit_vexapicall
    
    def visit_functioncall(self, node: FunctionCall):
        """Check if a regular function call is actually a VEX API call"""
        # Try to determine if this is a VEX function call
        function_name = None
        
        # Direct function name
        if isinstance(node.function, Identifier):
            function_name = node.function.name
        
        # Method call like motor.spin()
        elif isinstance(node.function, AttributeAccess):
            obj = node.function.object
            if isinstance(obj, Identifier):
                function_name = f"{obj.name}.{node.function.attribute}"
        
            # Check if this is a known VEX function
            if function_name:
                is_vex_function = False
                
                # Check if this is a method call on a known object type
                if '.' in function_name:
                    obj_name, method_name = function_name.split('.', 1)
                    
                    # First check if the method exists in the registry
                    if registry_api.get_function(method_name):
                        is_vex_function = True
                    else:
                        # Try to check if it's a method on any known object type
                        from ..types.objects import MOTOR, TIMER, BRAIN, CONTROLLER
                        for obj_type in [MOTOR, TIMER, BRAIN, CONTROLLER]:
                            if registry_api.get_method(obj_type, method_name):
                                is_vex_function = True
                                break
                # Or check if it's a direct function
                elif registry_api.get_function(function_name):
                    is_vex_function = True
                
            if is_vex_function:
                # Convert to VexAPICall and validate
                vex_call = VexAPICall(
                    node.function, 
                    node.args, 
                    node.keywords, 
                    node.location
                )
                valid, error = vex_call.validate()
                if not valid and error:
                    self.errors.append((vex_call, error))
        
        # Still visit children
        for child in node.get_children():
            self.visit(child)
        
        return self.errors

def validate_vex_functions(ast: Program) -> List[Tuple[VexAPICall, str]]:
    """Validate all VEX function calls in the AST"""
    validator = VexFunctionValidator()
    return validator.visit(ast)
