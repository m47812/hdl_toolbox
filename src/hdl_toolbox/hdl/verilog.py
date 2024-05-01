import re

from .hdl import HDL_Module
from .signal import VerilogSignal
from .templates import VerilogEntityTemplate, VerilogInstanceTemplate

class Verilog_Module(HDL_Module):
    def __init__(self, source = None):
        if source is not None:
            source_no_comment = self._remove_comments(source)
            self.entity_name, generics, signals = self._extract_entity_content(source_no_comment)
            self.signals = [VerilogSignal(signal_str.strip()) for signal_str in signals]
            self.generics = [VerilogSignal(generic_str.strip()) for generic_str in generics]
        else:
            self.entity_name = ""
            self.generics = []
            self.signals = []

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
        if len(self.generics) > 0:
            genrics_str = self._signals_entity_format(self.generics)
        else:
            genrics_str = None
        signals_str = self._signals_entity_format(self.signals)
        template = VerilogEntityTemplate(
            self.entity_name,
            signals_str,
            genrics_str
        )
        return str(template)
    
    @property
    def component_string(self):
        raise AttributeError("Component declarations are not existent in Verilog")
    def signal_declaration_string(self, en_constants=True, en_signals=True):
        raise NotImplementedError("Can not be executed in the base class")
    def instance_string(self, instance_name=None):
        if len(self.generics) > 0:
            genrics_str = self._signals_instance_format(self.generics)
        else:
            genrics_str = None
        signals_str = self._signals_instance_format(self.signals)
        if instance_name is None:
            instance_name = "inst_" + self.entity_name
        template = VerilogInstanceTemplate(
            instance_name, 
            self.entity_name,
            signals_str,
            genrics_str
        )
        return str(template)
    
    def _signals_entity_format(self, signals):
        signal_str = ""
        for signal in signals[:-1]:
            signal_str = signal_str + signal.entity_string + ",\n"
        signal_str = signal_str + signals[-1].entity_string
        return signal_str
    
    def _signals_instance_format(self, signals):
        signal_str = ""
        for signal in signals[:-1]:
            signal_str = signal_str + signal.instance_string() + ",\n"
        signal_str = signal_str + signals[-1].instance_string()
        return signal_str
    def to_verilog(self):
        return self
    def to_vhdl(self):
        from .vhdl import VHDL_Module
        vhdl_module = VHDL_Module()
        vhdl_module.entity_name = self.entity_name
        vhdl_module.signals = [signal.to_vhdl() for signal in self.signals]
        vhdl_module.generics = [signal.to_vhdl() for signal in self.generics]
        return vhdl_module