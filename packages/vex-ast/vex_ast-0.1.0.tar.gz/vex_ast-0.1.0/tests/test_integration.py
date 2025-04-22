# tests/test_integration.py
import pytest
from vex_ast import parse_string
from vex_ast.visitors.printer import PrintVisitor
from vex_ast.visitors.analyzer import NodeCounter, VariableCollector

class TestIntegration:
    def test_full_program_parse(self):
        # A complete program with multiple features
        code = """
        def drive_forward(speed, time_ms):
            # Set both motors to the specified speed
            left_motor.set_velocity(speed, PERCENT)
            right_motor.set_velocity(speed, PERCENT)
            
            # Start the motors
            left_motor.spin(FORWARD)
            right_motor.spin(FORWARD)
            
            # Wait for the specified time
            wait(time_ms, MSEC)
            
            # Stop the motors
            left_motor.stop()
            right_motor.stop()
            
            return True

        # Main program
        def main():
            # Display welcome message
            brain.screen.print("Robot starting...")
            wait(1, SECONDS)
            
            # Drive forward at 50% speed for 2 seconds
            success = drive_forward(50, 2000)
            
            if success:
                brain.screen.print("Drive completed!")
            else:
                brain.screen.print("Drive failed!")
            
            return 0
        """
        
        # Just test that parsing doesn't raise exceptions
        ast = parse_string(code)
        
        # Check that we have two function definitions
        assert len(ast.body) == 2
        assert ast.body[0].__class__.__name__ == "FunctionDefinition"
        assert ast.body[1].__class__.__name__ == "FunctionDefinition"
        assert ast.body[0].name == "drive_forward"
        assert ast.body[1].name == "main"
        
        # Test that visitors work with the complex AST
        printer = PrintVisitor()
        result = printer.visit(ast)
        assert isinstance(result, str)
        
        counter = NodeCounter()
        count = counter.visit(ast)
        assert count > 30  # Should have many nodes
        
        collector = VariableCollector()
        variables = collector.visit(ast)
        assert "left_motor" in variables
        assert "right_motor" in variables
        assert "brain" in variables
        assert "success" in variables