from typing import List

from ..hdl import HDL_Module
from ..hdl.signal import SignalDirection, Signal
from ..hdl.templates import VHDLArchitectureTemplate
from ..gui import EntityPanel, TopLevelModulePanel, TopLevelModuleApplication

class TopLevelCreator:
    def __init__(self, hdl_modules : List[HDL_Module], toplevel_entity : HDL_Module = None) -> None:
        self.hdl_modules = hdl_modules
        self.connections = []
        self.top_level_connections = []
        self.toplevel_entity = toplevel_entity

    def execute(self, auto_connect=False):
        app = TopLevelModuleApplication()
        app.create_application()
        parent_panel = self._create_panel()
        if auto_connect:
            self._auto_connect(parent_panel)
        app.exec_as_application(parent_panel)
    
    def execute_as_dialog(self, auto_connect=False):
        app = TopLevelModuleApplication()
        parent_panel = self._create_panel()
        if auto_connect:
            self._auto_connect(parent_panel)
        app.exec_as_dialog(parent_panel)

    def _create_panel(self):
        parent_panel = TopLevelModulePanel(self.add_connection_callback)
        if self.toplevel_entity is not None:
           parent_panel.addEntityPanel(
                self.toplevel_entity.entity_name,
                [signal for signal in self.toplevel_entity.signals if signal.direction == SignalDirection.In or signal.direction == SignalDirection.InOut],
                [signal for signal in self.toplevel_entity.signals if signal.direction == SignalDirection.Out],
                is_top_level_entity=True
            )
        for module in self.hdl_modules:
            parent_panel.addEntityPanel(
                module.entity_name,
                [signal for signal in module.signals if signal.direction == SignalDirection.In or signal.direction == SignalDirection.InOut],
                [signal for signal in module.signals if signal.direction == SignalDirection.Out]
            )  
        return parent_panel
    
    def _auto_connect(self, top_panel, en_signal_mapping=True, en_generic_mapping=True):
        if not self.toplevel_entity is None:
            if en_signal_mapping:
                for top_signal in self.toplevel_entity.signals:
                    for module in self.hdl_modules:
                        for signal in module.signals:
                            if top_signal.name == signal.name and top_signal.direction == signal.direction:
                                self.add_connection_callback(top_signal, signal)
                signals_connected = [connection[0] for connection in self.top_level_connections]
                signals_connected.extend([connection[1] for connection in self.top_level_connections])
                top_panel.set_signal_connected_status(signals_connected, set_connected=True)
            if en_generic_mapping:
                for top_generic in self.toplevel_entity.generics:
                    for module in self.hdl_modules:
                        for generic in module.generics:
                            if top_generic.name == generic.name:
                                self.add_connection_callback(top_generic, generic)
    
    def add_connection_callback(self, source, destination):
        if self.toplevel_entity is not None:
            if source in self.toplevel_entity.signals:
                self.top_level_connections.append((source, destination))
            elif destination in self.toplevel_entity.signals:
                self.top_level_connections.append((destination, source)) #Toplevel is always at source position
            else:
               self.connections.append((source, destination)) 
        else:      
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
        for source, dest in self.top_level_connections:
            source.connected_signal = source
            dest.connected_signal = source
        components = ""
        instances = ""
        for module in self.hdl_modules:
            components = components + module.component_string + "\n\n"
            instances = instances + module.instance_string() + "\n\n"
        template = VHDLArchitectureTemplate(
            entity_name= "top_level" if self.toplevel_entity is None else self.toplevel_entity.entity_name,
            instances = instances, 
            components = components,
            signals = signals 
        )
        return str(template)