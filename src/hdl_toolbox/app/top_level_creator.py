from typing import List

from ..hdl import HDL_Module
from ..hdl.signal import SignalDirection, Signal
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
        