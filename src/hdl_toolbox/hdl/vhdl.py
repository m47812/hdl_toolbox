import re

from .hdl import HDL_Module
from .signal import SignalDirection, VHDLSignal
from .signal_types import VHDLSignalType, VHDLRangeSignalType, VHDLVectorSignalType, VHDLSignalRange

class VHDL_Module(HDL_Module):
    def __init__(self):
        self.signals = []

    def from_source_code(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _extract_signal_strings(self, source):
        return re.findall(r'\w+\s*:\s*(?:in|out|inout)\s*\w+\s*(?:\(.*\)|range\s+.+?to.*?)?(?=(?:;|\)))', source, re.IGNORECASE)

    def _separate_signal_into_subcomponents(self, signal_str) -> VHDLSignal:
        signal_name = re.findall(r'\w+(?=\s*:)', signal_str, re.IGNORECASE)[0]
        signal_direction = re.findall(r'(?<=:)\s*\w+', signal_str, re.IGNORECASE)[0].strip().lower()
        if signal_direction == "in":
            signal_direction = SignalDirection.In
            signal_type = re.findall(r'(?<=in)\s*\w+', signal_str, re.IGNORECASE)[0].strip()
        elif signal_direction == "out":
            signal_direction = SignalDirection.Out
            signal_type = re.findall(r'(?<=out)\s*\w+', signal_str, re.IGNORECASE)[0].strip()
        elif signal_direction == "inout":
            signal_direction = SignalDirection.InOut
            signal_type = re.findall(r'(?<=inout)\s*\w+', signal_str, re.IGNORECASE)[0].strip()
        else:
            raise ValueError("Unknown signal direction was:" + signal_direction)
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
        return VHDLSignal(signal_name, signal_type_object, signal_direction)