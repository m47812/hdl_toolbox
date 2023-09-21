import re

from .hdl import HDL_Module
from .signal import SignalDirection, VHDLSignal
from .signal_types import VHDLSignalType, VHDLRangeSignalType, VHDLVectorSignalType

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
    
    def _remove_comments(self, source):
        comments = re.findall(r'--.*', source)
        source_no_comments = source
        for comment in comments:
            source_no_comments = source_no_comments.replace(comment, "")
        return source_no_comments