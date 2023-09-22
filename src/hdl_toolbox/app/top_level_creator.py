from typing import List

from ..hdl import HDL_Module
from ..hdl.signal import SignalDirection, Signal
from ..hdl.templates import VHDLArchitectureTemplate
from ..gui import EntityPanel, TopLevelModulePanel, TopLevelModuleApplication

class TopLevelCreator:
    def __init__(self, hdl_modules : List[HDL_Module]) -> None:
        self.hdl_modules = hdl_modules
        self.connections = []

    def execute(self):
        app = TopLevelModuleApplication()
        parent_panel = TopLevelModulePanel(self.add_connection_callback)
        for module in self.hdl_modules:
            parent_panel.addEntityPanel(
                module.entity_name,
                [signal for signal in module.signals if signal.direction == SignalDirection.In or signal.direction == SignalDirection.InOut],
                [signal for signal in module.signals if signal.direction == SignalDirection.Out]
            )
        app.top_level_connector_execute(parent_panel)
    
    def add_connection_callback(self, source, destination):
        self.connections.append((source, destination))
        print("Source: " + source.name + " Destination: " + destination.name)
    
    def generate_architecture(self): 
        signals = ""
        signals_declared = []
        for source, dest in self.connections:
            source.connected_signal = source
            dest.connected_signal = source
            if source not in signals_declared:
                signals = signals + source.declaration_string + "\n"
                signals_declared.append(source)
        components = ""
        instances = ""
        for module in self.hdl_modules:
            components = components + module.component_string + "\n\n"
            instances = instances + module.instance_string() + "\n\n"
        template = VHDLArchitectureTemplate(
            instances = instances, 
            components = components,
            signals = signals 
        )
        return str(template)