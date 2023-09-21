import re

from .hdl import HDL_Module
from .signal import SignalDirection, VHDLSignal
from .signal_types import VHDLSignalType, VHDLRangeSignalType, VHDLVectorSignalType, VHDLSignalRange

class VHDL_Module(HDL_Module):
    def __init__(self):
        self.signals = []

    def from_source_code(self, source):
        signals, generics = self._extract_signals_and_generics_strings(source)
    
    def _extract_signals_and_generics_strings(self, source):
        source_no_comments = self._remove_comments(source)
        entity_str = re.findall(r'entity.*?end(?:\s+entity)?\s+\w+\s*;', source_no_comments, re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
        port_str = re.findall(r'port.*?(?:end|generic)', entity_str, re.IGNORECASE| re.DOTALL | re.MULTILINE)
        generic_str = re.findall(r'generic.+?(?:port|end)', entity_str,re.IGNORECASE | re.DOTALL | re.MULTILINE)
        if len(generic_str) != 0:
            generics = self._extract_signal_strings(generic_str[0])
        if len(port_str) != 0:
            signals = self._extract_signal_strings(port_str[0])
        return signals, generics

    def _extract_signal_strings(self, source):
        return re.findall(r'\w+\s*:\s*(?:in|out|inout)?\s*\w+\s*(?:\(.*\)|range\s+.+?to.*?)?(?:\s*:=.+?)?(?=(?:;|\s*\n\s*\)))', source, re.IGNORECASE)

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
    
    def _remove_comments(self, source):
        comments = re.findall(r'--.*', source)
        source_no_comments = source
        for comment in comments:
            source_no_comments = source_no_comments.replace(comment, "")
        return source_no_comments