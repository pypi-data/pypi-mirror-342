# tests/test_vex_nodes.py
import pytest
from vex_ast.ast.vex_nodes import (
    VexAPICall, MotorControl, SensorReading, 
    TimingControl, DisplayOutput
)
from vex_ast.ast.expressions import Identifier, KeywordArgument

class TestVexNodes:
    def test_vex_api_call(self):
        func = Identifier("vex_function")
        args = [Identifier("arg1"), Identifier("arg2")]
        
        vex_call = VexAPICall(func, args)
        assert vex_call.function == func
        assert vex_call.args == args
        
    def test_motor_control(self):
        func = Identifier("set_motor")
        args = [Identifier("motor1"), Identifier("speed")]
        
        motor_ctrl = MotorControl(func, args)
        assert motor_ctrl.function == func
        assert motor_ctrl.args == args
        
    def test_sensor_reading(self):
        func = Identifier("get_sensor")
        args = [Identifier("sensor1")]
        
        sensor = SensorReading(func, args)
        assert sensor.function == func
        assert sensor.args == args
        
    def test_timing_control(self):
        func = Identifier("wait")
        args = [Identifier("duration")]
        
        timing = TimingControl(func, args)
        assert timing.function == func
        assert timing.args == args
        
    def test_display_output(self):
        func = Identifier("print_to_display")
        args = [Identifier("message")]
        
        display = DisplayOutput(func, args)
        assert display.function == func
        assert display.args == args