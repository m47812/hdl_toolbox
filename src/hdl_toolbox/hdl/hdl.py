""" This file is part of the HDL Toolbox distribution (https://github.com/m47812/hdl_toolbox).
Copyright (c) 2024 Robin Müller.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>. """

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
    
    def invert_direction(self):
        for signal in self.signals:
            signal.invert_direction()

    def signal_declaration_string(self, en_constants=True, en_signals=True):
        raise NotImplementedError("Can not be executed in the base class")
    def instance_string(self, instance_name=None):
        raise NotImplementedError("Can not be executed in the base class")
    def to_verilog(self):
        raise NotImplementedError("Can not be executed in the base class")
    def to_vhdl(self):
        raise NotImplementedError("Can not be executed in the base class")