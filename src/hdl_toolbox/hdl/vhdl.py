import re

from .hdl import HDL_Module
from .signal import VHDLSignal
from .templates import VHDLEntityTemplate, VHDLComponentTemplate, VHDLInstanceTemplate

class VHDL_Module(HDL_Module):
    def __init__(self, source = None):
        if source is not None:
            source_no_comment = self._remove_comments(source)
            self.entity_name, generics, signals = self._extract_entity_content(source_no_comment) 
            self.signals = [VHDLSignal(signal_str) for signal_str in signals]
            self.generics = [VHDLSignal(generic_str) for generic_str in generics]
    
    def _extract_entity_content(self, source):
        entity_name = re.findall(r'entity\s+(\w+)\s+is', source, re.IGNORECASE)[0]
        entity_str = re.findall(r'entity.*?end(?:\s+entity)?\s+'+ entity_name +r'\s*;', source, re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
        entity_str = re.sub(r'entity\s+\w+\s+is', '', entity_str, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
        entity_str = re.sub(r'end(?:\s+entity)?\s+\w+\s*;', '', entity_str, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
        subcomponents = re.split(r'(generic|port)[\n|\s]*\(', entity_str, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
        signals, generics =  [], []
        for i, component in enumerate(subcomponents):
            if component.lower() == "port":
                port_content = re.findall(r'(.*)\)[\n|\s]*;', subcomponents[i+1], re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
                signals = re.split(r'(?:;)', port_content)
            if component.lower() == "generic":
                generic_content = re.findall(r'(.*)\)[\n|\s]*;', subcomponents[i+1], re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
                generics = re.split(r'(?:;)', generic_content)
        return entity_name, generics, signals
    
    def _remove_comments(self, source):
        return re.sub(r'--.*?\n', '', source)
    
    @property
    def entity_string(self):
        if len(self.generics) > 0:
            genrics_str = self._signals_entity_format(self.generics)
        else:
            genrics_str = None
        signals_str = self._signals_entity_format(self.signals)
        template = VHDLEntityTemplate(
            self.entity_name,
            signals_str,
            genrics_str
        )
        return str(template)
    
    @property
    def component_string(self):
        if len(self.generics) > 0:
            genrics_str = self._signals_entity_format(self.generics)
        else:
            genrics_str = None
        signals_str = self._signals_entity_format(self.signals)
        template = VHDLComponentTemplate(
            self.entity_name,
            signals_str,
            genrics_str
        )
        return str(template)

    def signal_declaration_string(self, en_constants=True, en_signals=True):
        constants_str, signal_str = "", ""
        if en_constants and len(self.generics) > 0:
            for generic in self.generics:
                constants_str += generic.constant_declaration_string + "\n"
        if en_signals and len(self.signals) > 0:
            for signal in self.signals:
                signal_str += signal.declaration_string + "\n"
        return constants_str + signal_str

    def instance_string(self, instance_name=None):
        if len(self.generics) > 0:
            genrics_str = self._signals_instance_format(self.generics)
        else:
            genrics_str = None
        signals_str = self._signals_instance_format(self.signals)
        if instance_name is None:
            instance_name = "inst_" + self.entity_name
        template = VHDLInstanceTemplate(
            instance_name, 
            self.entity_name,
            signals_str,
            genrics_str
        )
        return str(template)
        
    def _signals_entity_format(self, signals):
        signal_str = ""
        for signal in signals[:-1]:
            signal_str = signal_str + signal.entity_string + ";\n"
        signal_str = signal_str + signals[-1].entity_string
        return signal_str
    
    def _signals_instance_format(self, signals):
        signal_str = ""
        for signal in signals[:-1]:
            signal_str = signal_str + signal.instance_string() + ",\n"
        signal_str = signal_str + signals[-1].instance_string()
        return signal_str