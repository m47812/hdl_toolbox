from enum import IntEnum
import re

from .signal_types import SignalType, VHDLVectorSignalType, VHDLRangeSignalType, VHDLSignalType 
from .signal_range import VHDLSignalRange

class SignalDirection:
    In = 0
    Out = 1
    InOut = 2
class Signal:
    def __init__(self, name, signal_type, direction : SignalDirection = None, default_value = None):
        self.name = name
        self.signal_type : SignalType = signal_type
        self.direction : SignalDirection = direction
        self.default_value = default_value
        self.connected_signal = None

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

class VHDLSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super().__init__(name, signal_type, direction)

        """Generates Object from signal String
        """
    def __init__(self, signal_str):
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

class VerilogSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super().__init__(name, signal_type, direction)

    @property
    def entity_string(self):
        direction_str = ""
        if self.direction == SignalDirection.In:
            direction_str = "input "
        elif self.direction == SignalDirection.Out:
            direction_str = "output "
        elif self.direction == SignalDirection.InOut:
            direction_str = "inout "
        return direction_str + self.signal_type.string + self.name

    def instance_string(self):
        return "." + self.name + "(#X)"

    @property
    def declaration_string(self):
        return "wire " + self.signal_type.string + self.name