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

    @property
    def entity_string(self):
        raise NotImplemented("EntityString is not defined for the base class")

    def instance_string(self):
        raise NotImplemented("InstanceString is not defined for the base class")
    def instance_string(self, connected_signal):
        raise NotImplemented("InstanceString is not defined for the base class")

    @property
    def declaration_string(self):
        raise NotImplemented("declaration_string is not defined for the base class")

class VHDLSignal(Signal):
    def __init__(self, name, signal_type, direction : SignalDirection = None):
        super().__init__(name, signal_type, direction)

        """Generates Object from signal String
        """
    def __init__(self, signal_str):
        signal_name = re.findall(r'\w+(?=\s*:)', signal_str, re.IGNORECASE)[0]
        signal_direction = re.findall(r'(?<=:)\s*\w+', signal_str, re.IGNORECASE)[0].strip().lower()
        if signal_direction == "in":
            signal_direction = SignalDirection.In
        elif signal_direction == "out":
            signal_direction = SignalDirection.Out
        elif signal_direction == "inout":
            signal_direction = SignalDirection.InOut
        else:
            raise ValueError("Unknown signal direction was:" + signal_direction)
        signal_type = re.findall(r'(?:in|out|inout)\s*(\w+)', signal_str, re.IGNORECASE)[0].strip()
        range_type_range = re.findall(r'(?<=range)\s+.+?to.*', signal_str, re.IGNORECASE)
        vector_type_range = re.findall(r'\(.+\)', signal_str, re.IGNORECASE)
        if len(range_type_range) == 0 and len(vector_type_range) > 0:
            vector_type_range = vector_type_range[0].strip().lower()
            #Vector Type
            if "downto" in vector_type_range:
                upper = re.findall(r'(?<=\().+?(?=downto)', vector_type_range, re.IGNORECASE)[0].strip()
                lower = re.findall(r'(?<=downto).+(?=\))', vector_type_range, re.IGNORECASE)[0].strip()
                range_object = VHDLSignalRange(lower, upper, "downto")
                signal_type_object = VHDLVectorSignalType(signal_type, range_object)
            elif "to" in vector_type_range:
                lower = re.findall(r'.+?(?:to)', vector_type_range, re.IGNORECASE)[0].strip()
                upper = re.findall(r'(?<=to).+', vector_type_range, re.IGNORECASE)[0].strip()
                range_object = VHDLSignalRange(lower, upper, "to")
                signal_type_object = VHDLVectorSignalType(signal_type, range_object)
            else:
                raise ValueError("Invalid Range Expression:" + vector_type_range)
        elif len(range_type_range) > 0 and len(vector_type_range) == 0:
            #Range Type
            range_type_range = range_type_range[0].strip().lower()
            lower = re.findall(r'.+?(?=to)', range_type_range, re.IGNORECASE)[0].strip()
            upper = re.findall(r'(?<=to).+', range_type_range, re.IGNORECASE)[0].strip()
            range_object = VHDLSignalRange(lower, upper, "to")
            signal_type_object = VHDLRangeSignalType(signal_type, range_object)
        else:
            #Single Bit Type
            signal_type_object = VHDLSignalType(signal_type)
        super().__init__(signal_name, signal_type_object, signal_direction)

    @property
    def entity_string(self):
        if self.direction is None:
            return self.name + " : " + self.signal_type.string
        else:
            if self.direction == SignalDirection.In:
                direction_str = "in"
            elif self.direction == SignalDirection.Out:
                direction_str = "out"
            elif self.direction == SignalDirection.InOut:
                direction_str = "inout"
            return self.name + " : " + direction_str + " " + self.signal_type.string

    def instance_string(self):
        return self.name + " => #X"

    def instance_string(self, connected_signal:Signal):
        return self.name + " => " + connected_signal.name

    @property
    def declaration_string(self):
        return "signal " + self.name + " : " + self.signal_type.string

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

    def instance_string(self, connected_signal:Signal):
        return "." + self.name + "(" + connected_signal.name + ")"

    @property
    def declaration_string(self):
        return "wire " + self.signal_type.string + self.name