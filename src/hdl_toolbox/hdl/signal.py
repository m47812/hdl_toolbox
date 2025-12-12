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

from enum import IntEnum
import re

from .signal_types import SignalType, VHDLVectorSignalType, VHDLRangeSignalType, VHDLSignalType, VerilogSignalType
from .signal_range import VHDLSignalRange, VerilogSignalRange

class SignalDirection:
    In = 0
    Out = 1
    InOut = 2

    INVERT = {
        0 : 1,  #In to Out
        1 : 0,  #Out to In
        2 : 2   #Inout to Inout
    }

class Signal:
    def __init__(self, name, signal_type, direction : SignalDirection = None, default_value = None):
        self.name = name
        self.signal_type : SignalType = signal_type
        self.direction : SignalDirection = direction
        self.default_value = default_value
        self.connected_signal = None

    def invert_direction(self):
        self.direction : SignalDirection = SignalDirection.INVERT[self.direction]

    @property
    def entity_string(self):
        raise NotImplemented("EntityString is not defined for the base class")
    
    @property
    def declaration_string(self):
        raise NotImplemented("declaration_string is not defined for the base class")
    
    def instance_string(self):
        raise NotImplemented("InstanceString is not defined for the base class")

    @property
    def constant_declaration_string(self):
        raise NotImplemented("constant_declaration_string is not defined for the base class")
    def to_verilog(self):
        raise NotImplementedError("Can not be executed in the base class")
    def to_vhdl(self):
        raise NotImplementedError("Can not be executed in the base class")

class VHDLSignal(Signal):
    def __init__(self,signal_str=None, name=None, signal_type=None, direction : SignalDirection = None, default_value = None):
        if signal_str is None:
            super().__init__(name, signal_type, direction, default_value)
        else:
            signal_name = re.findall(r'\w+(?=\s*:)', signal_str, re.IGNORECASE)[0]
            super().__init__(
                signal_name,
                self._extract_signal_type(signal_str),
                self._extract_signal_direction(signal_str),
                self._extract_default_value(signal_str)
            )
        
    def _extract_signal_direction(self, signal_str) -> SignalDirection:
        signal_direction = re.findall(r'(?<=:)\s*\w+', signal_str, re.IGNORECASE)[0].strip().lower()
        if signal_direction == "in":
            return SignalDirection.In
        elif signal_direction == "out":
            return SignalDirection.Out
        elif signal_direction == "inout":
            return SignalDirection.InOut
        else:
            return None

    def _extract_signal_type(self, signal_str) -> VHDLSignalType:
        signal_type = re.findall(r':\s*(?:(?:in|out|inout)\s+)?\s*(\w+)', signal_str, re.IGNORECASE)[0].strip()
        range_type_range = re.findall(r'(?<=range)\s+.+?to.*', signal_str, re.IGNORECASE)
        vector_type_range = re.findall(r'\(.+\)', signal_str, re.IGNORECASE)
        if len(range_type_range) == 0 and len(vector_type_range) > 0:
            #Vector Type
            vector_type_range = vector_type_range[0].strip().lower()
            return VHDLVectorSignalType(signal_type, VHDLSignalRange(vector_type_range))
        elif len(range_type_range) > 0 and len(vector_type_range) == 0:
            #Range Type
            range_type_range = range_type_range[0].strip().lower()
            return VHDLRangeSignalType(signal_type, VHDLSignalRange(range_type_range))
        else:
            #Single Bit Type
            return VHDLSignalType(signal_type)

    def _extract_default_value(self, signal_str):
        default_value = re.findall(r':=\s*(\w+)', signal_str, re.IGNORECASE)
        if len(default_value) != 0:
            return default_value[0]
        else:
            return None

    @property
    def entity_string(self):
        if self.direction is None:
            ret_string = self.name + " : " + self.signal_type.string
        else:
            if self.direction == SignalDirection.In:
                direction_str = "in"
            elif self.direction == SignalDirection.Out:
                direction_str = "out"
            elif self.direction == SignalDirection.InOut:
                direction_str = "inout"
            ret_string = self.name + " : " + direction_str + " " + self.signal_type.string
        if self.default_value is not None:
            ret_string = ret_string + " := " + self.default_value
        return ret_string
    
    @property
    def declaration_string(self):
        return "signal " + self.name + " : " + self.signal_type.string + ";"
    
    def instance_string(self):
        if self.connected_signal is None:
            return self.name + " => "
        else:
            return self.name + " => " + self.connected_signal.name

    @property
    def constant_declaration_string(self):
        default_val = self.default_value
        if self.default_value is None:
            default_val = "INSERT_DEFAULT_VALUE_HERE"
        return "constant " + self.name + " : " + self.signal_type.string + " := " + default_val + ";"
    def to_verilog(self):
        if self.direction is None:
            return VerilogSignal(name=self.name, signal_type=self.signal_type.to_verilog(), is_parameter=True, is_reg=False, direction=self.direction, default_value=self.default_value)
        else:
            return VerilogSignal(name=self.name, signal_type=self.signal_type.to_verilog(), is_parameter=False, is_reg=False, direction=self.direction, default_value=self.default_value)
    def to_vhdl(self):
        return self

class VerilogSignal(Signal):
    def __init__(self, signal_str=None, name=None, signal_type=None, is_parameter=None, is_reg=None,  direction : SignalDirection = None, default_value = None):
        if signal_str is None:
            super().__init__(name, signal_type, direction, default_value)
            self.is_parameter = is_parameter
            self.is_reg = is_reg
        else:
            self.is_reg = len(re.findall(r'(?<!\w)reg\s', signal_str, re.IGNORECASE)) != 0
            signal_str = re.sub(r'(?<!\w)reg\s', "", signal_str, flags=re.IGNORECASE)
            signal_str = re.sub(r'(?<!\w)wire\s', "", signal_str, flags=re.IGNORECASE)
            signal_name = re.findall(r'(?:(?:input|output|inout|parameter)\s+)(?:signed\s+)?(?:\[.*?\])?\s*(\w+)', signal_str, re.IGNORECASE)[0]
            self.is_parameter = len(re.findall(r'(?<!\w)parameter\s', signal_str, re.IGNORECASE)) != 0
            super().__init__(
                signal_name,
                self._extract_signal_type(signal_str),
                self._extract_signal_direction(signal_str),
                self._extract_default_value(signal_str)
            )    

    def _extract_signal_direction(self, signal_str) -> SignalDirection:
        signal_direction = re.findall(r'(?<!\w)(input|output|inout)\s+', signal_str, re.IGNORECASE)
        if len(signal_direction) == 0:
            return None
        signal_direction = signal_direction[0]
        if signal_direction == "input":
            return SignalDirection.In
        elif signal_direction == "output":
            return SignalDirection.Out
        elif signal_direction == "inout":
            return SignalDirection.InOut
        else:
            return None
        
    def _extract_signal_type(self, signal_str) -> VerilogSignalType:
        range_expr = re.findall(r'\[(.*?)\]', signal_str, re.IGNORECASE)
        range_obj = None
        if len(range_expr) != 0:
            upper = re.findall(r'(.+):', range_expr[0], re.IGNORECASE)[0].strip()
            lower = re.findall(r':(.+)', range_expr[0], re.IGNORECASE)[0].strip()
            signal_str = re.sub(r'\[.*?\]', "", signal_str)
            range_obj = VerilogSignalRange(lower, upper)
        is_signed = len(re.findall(r'signed', signal_str, re.IGNORECASE)) != 0
        return VerilogSignalType(is_signed, range_obj)
    
    def _extract_default_value(self, signal_str):
        default_value = re.findall(r'\=(.*)', signal_str, re.IGNORECASE)
        if len(default_value) != 0:
            return default_value[0].strip()
        else:
            return None

    @property
    def entity_string(self):
        entity_str = ""
        if self.is_parameter:
            entity_str += "parameter "
        if self.direction == SignalDirection.In:
            entity_str = "input "
        elif self.direction == SignalDirection.Out:
            entity_str = "output "
        elif self.direction == SignalDirection.InOut:
            entity_str = "inout "
        if self.is_reg:
            entity_str +=  "reg "
        entity_str += self.signal_type.string + self.name
        if self.default_value is not None:
            entity_str += " = " + self.default_value
        return entity_str

    def instance_string(self):
        if self.connected_signal is None:
            return "." + self.name + "()"
        else:
            return "." + self.name + "(" + self.connected_signal.name + ")"

    @property
    def declaration_string(self):
        return "wire " + self.name + ";"
    
    @property
    def constant_declaration_string(self):
        default_val = self.default_value
        if self.default_value is None:
            default_val = "INSERT_DEFAULT_VALUE_HERE"
        return "localparam " + self.name + " = " + default_val + ";"

    def to_verilog(self):
        return self
    def to_vhdl(self):
        return VHDLSignal(name=self.name, signal_type=self.signal_type.to_vhdl(self.is_parameter), direction=self.direction, default_value=self.default_value)