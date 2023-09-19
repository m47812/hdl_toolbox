import re

from .hdl import HDL_Module

class VHDL_Module(HDL_Module):
    def __init__(self):
        self.signals = []

    def from_source_code(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _extract_signal_strings(self, source):
        return re.findall(r'\w+\s*:\s*(?:in|out|inout)\s*\w+\s*(?:\(.*?\)|range\s+.+?to.*?(?=(?:;|\))))?', source, re.IGNORECASE)