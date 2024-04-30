from typing import List

from .signal import Signal, SignalDirection
from .templates import COCOTBInterfaceTemplate

class HDL_Module:
    def __init__(self):
        self.signals : List[Signal] = []
        self.generics : List[Signal] = []
        self.entity_name = ""
    
    @property
    def entity_string(self):
        raise NotImplementedError("Can not be executed in the base class")
    @property
    def component_string(self):
        raise NotImplementedError("Can not be executed in the base class")

    @property
    def cocotb_interface_string(self):
        signal_string = "".join([
            "self." + signal.name + " = dut." + signal.name +"\n"
            for signal in self.signals
        ])
        inputs_string = "".join([
            "self." + signal.name + ".value = 0\n"
            for signal in self.signals
            if signal.direction == SignalDirection.In
        ])
        template = COCOTBInterfaceTemplate(self.entity_name, signal_string, inputs_string)
        return str(template)

    def signal_declaration_string(self, en_constants=True, en_signals=True):
        raise NotImplementedError("Can not be executed in the base class")
    def instance_string(self, instance_name=None):
        raise NotImplementedError("Can not be executed in the base class")