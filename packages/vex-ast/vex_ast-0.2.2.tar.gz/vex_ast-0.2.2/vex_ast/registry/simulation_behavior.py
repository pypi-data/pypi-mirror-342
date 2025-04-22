# vex_ast/registry/simulation_behavior.py
from enum import Enum, auto

class SimulationBehavior(Enum):
    """Categories of simulation behaviors for VEX functions"""
    AFFECTS_MOTOR = "AFFECTS_MOTOR"
    READS_SENSOR = "READS_SENSOR"
    AFFECTS_TIMING = "AFFECTS_TIMING"
    AFFECTS_DISPLAY = "AFFECTS_DISPLAY"