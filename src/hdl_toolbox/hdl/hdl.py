from typing import List

from .signal import Signal

class HDL_Module:
    def __init__(self):
        self.signals : List[Signal] = []
        self.generics : List[Signal] = []
        self.entity_name = ""

    def from_source_code(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _extract_signal_strings(self, source):
        raise NotImplementedError("from_source_code can not be executed in the base class")

    def _separate_signal_into_subcomponents(self, signal_str):
        raise NotImplementedError("_separate_signal_into_subcomponents can not be executed in the base class")
    
    @property
    def entity_string(self):
        raise NotImplementedError("Can not be executed in the base class")
    @property
    def component_string(self):
        raise NotImplementedError("Can not be executed in the base class")
    
    def instance_string(self, instance_name=None):
        raise NotImplementedError("Can not be executed in the base class")