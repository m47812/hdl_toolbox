from typing import List

from ..hdl import HDL_Module
from ..hdl.templates import VHDLArchitectureTemplate, VHDLEntityTemplate

class VHDLDontTouchTopLevelCreator:
    def __init__(self, hdl_modules : List[HDL_Module]):
        self.hdl_modules = hdl_modules
        for module in self.hdl_modules:
            for generic in module.generics:
                generic.connected_signal = generic
            for signal in module.signals:
                signal.connected_signal = signal

    def __str__(self):
        components = ""
        instances = ""
        signals = ""
        dont_touch_setting = "attribute dont_touch : string;\n"
        for module in self.hdl_modules:
            components += module.component_string + "\n\n"
            signals += module.signal_declaration_string() + "\n"
            instance_name = "inst_" + module.entity_name
            instances += module.instance_string(instance_name=instance_name) + "\n\n"
            dont_touch_setting += "attribute dont_touch of " + instance_name + " : label is \"true\";"
        signals += "\n" + dont_touch_setting
        template = VHDLArchitectureTemplate(
            instances=instances,
            components=components,
            signals=signals,
            entity_name="top_level_dts"
        )
        entity_template = VHDLEntityTemplate(
            entity_name="top_level_dts"
        )
        return str(entity_template) + "\n\n" + str(template)