import re

from .hdl import HDL_Module
from .signal import VerilogSignal

class Verilog_Module(HDL_Module):
    def __init__(self, source = None):
        if source is not None:
            source_no_comment = self._remove_comments(source)
            self.entity_name, generics, signals = self._extract_entity_content(source_no_comment)
            self.signals = [VerilogSignal(signal_str.strip()) for signal_str in signals]
            self.generics = [VerilogSignal(generic_str.strip()) for generic_str in generics]

    def _extract_entity_content(self, source):
        entity_name = re.findall(r'module\s+(\w+)\s*#?\s*\(', source, re.IGNORECASE)[0]
        entity_str = re.findall(r'module\s+\w+.*?(#?\(.*?\)\s*;)', source, re.IGNORECASE | re.DOTALL | re.MULTILINE)[0].strip()
        if entity_str[0] == "#":
            generics = re.findall(r'[\n\s]+(parameter\s+.*?)(?:,|\)[\n\s]*\()', entity_str, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            entity_str = re.sub(r'#\(.*?\)','', entity_str, flags=re.MULTILINE | re.DOTALL)
        else:
            generics = []
        signals = re.findall(r'\((.*)\)\s*;', entity_str, re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
        signals = re.split(r',', signals)
        return entity_name, generics, signals
    
    def _remove_comments(self, source):
        rm_block_comments = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL) #Remove block comments
        return re.sub(r'//.*?\n', '', rm_block_comments) #Remove line comments

    @property
    def entity_string(self):
        raise NotImplementedError("Can not be executed in the base class")
    @property
    def component_string(self):
        raise NotImplementedError("Can not be executed in the base class")
    def signal_declaration_string(self, en_constants=True, en_signals=True):
        raise NotImplementedError("Can not be executed in the base class")
    def instance_string(self, instance_name=None):
        raise NotImplementedError("Can not be executed in the base class")