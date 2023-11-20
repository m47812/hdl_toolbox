import re

from .hdl import HDL_Module
from .signal import VHDLSignal
from .templates import VHDLEntityTemplate, VHDLComponentTemplate, VHDLInstanceTemplate

class VHDL_Module(HDL_Module):
    def __init__(self, source = None):
        if source is not None:
            signals, generics = self._extract_signals_and_generics_strings(source)
            self.signals = [VHDLSignal(signal_str) for signal_str in signals]
            self.generics = [VHDLSignal(generic_str) for generic_str in generics]
            self.entity_name = re.findall(r'entity\s+(\w+)\s+is', source, re.IGNORECASE)[0]
    
    def _extract_signals_and_generics_strings(self, source):
        source_no_comments = self._remove_comments(source)
        entity_str = re.findall(r'entity.*?end(?:\s+entity)?\s+\w+\s*;', source_no_comments, re.IGNORECASE | re.DOTALL | re.MULTILINE)[0]
        port_str = re.findall(r'port[\n|\s]*?\(.*?(?:end|generic)', entity_str, re.IGNORECASE| re.DOTALL | re.MULTILINE)
        generic_str = re.findall(r'generic[\n|\s]*?\(.+?(?=(?:port[\n|\s]*?\(|end))', entity_str,re.IGNORECASE | re.DOTALL | re.MULTILINE)
        if len(generic_str) != 0:
            generics = self._extract_signal_strings(generic_str[0])
        else:
            generics = []
        if len(port_str) != 0:
            signals = self._extract_signal_strings(port_str[0])
        else:
            signals = []
        return signals, generics

    def _extract_signal_strings(self, source):
        return re.findall(r'\w+\s*:\s*(?:in|out|inout)?\s*\w+\s*(?:\(.*\)|range\s+.+?to.*?)?(?:\s*:=.+?)?(?=(?:;|\s*\n\s*\)))', source, re.IGNORECASE)
    
    def _remove_comments(self, source):
        comments = re.findall(r'--.*', source)
        source_no_comments = source
        for comment in comments:
            source_no_comments = source_no_comments.replace(comment, "-- ")
        source_no_comments = source_no_comments.replace("-- ", "")
        return source_no_comments
    
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