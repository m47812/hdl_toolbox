from .template_manager import TemplateManager

class _VHDLComponentEntityTemplate(TemplateManager):
    def __init__(self, entity_name = None, port_signals = None, generic_signals = None) -> None:
        self._port_template = self.read_template_file_relative_path("./vhdl/entity_port.txt")
        self._generics_template = self.read_template_file_relative_path("./vhdl/entity_generics.txt")
        self.port_signals = port_signals
        self.generic_signals = generic_signals
        self.entity_name = entity_name
    
    def __str__(self):
        template = self._template
        template = template.replace("#ENTITY_NAME", self.entity_name)
        if self.generic_signals is not None:
            indented_generics = self.indent(self.generic_signals, 1)
            template = template.replace(
                "#GENERIC",
                self.indent(self._generics_template.replace("#SIGNALS", indented_generics), 1)
            )
        else:
            template = template.replace("#GENERIC", "")
        if self.port_signals is not None:
            template = template.replace(
                "#PORT",
                self.indent(self._port_template.replace("#SIGNALS", self.indent(self.port_signals, 1)), 1)
            )
        else:
            template = template.replace("#PORT", "")
        return template
    
class VHDLEntityTemplate(_VHDLComponentEntityTemplate):
    def __init__(self, entity_name = None, port_signals = None, generic_signals = None) -> None:
        super().__init__(entity_name, port_signals, generic_signals)
        self._template = self.read_template_file_relative_path("./vhdl/entity.txt")

class VHDLComponentTemplate(_VHDLComponentEntityTemplate):
    def __init__(self, entity_name = None, port_signals = None, generic_signals = None) -> None:
        super().__init__(entity_name, port_signals, generic_signals)
        self._template = self.read_template_file_relative_path("./vhdl/component.txt")

class VHDLInstanceTemplate(_VHDLComponentEntityTemplate):
    def __init__(self, instance_name,  entity_name, port_signals = None, generic_signals = None) -> None:
        self._template = self.read_template_file_relative_path("./vhdl/instance.txt")
        self._port_template = self.read_template_file_relative_path("./vhdl/instance_port.txt")
        self._generics_template = self.read_template_file_relative_path("./vhdl/instance_generics.txt")
        self.port_signals = port_signals
        self.generic_signals = generic_signals
        self.entity_name = entity_name
        self.instance_name = instance_name
    
    def __str__(self):
        string = super(VHDLInstanceTemplate, self).__str__() 
        return string.replace("#INSTANCE_NAME", self.instance_name)
    
class VHDLArchitectureTemplate(TemplateManager):
    def __init__(self, entity_name="top_level", instances=None, components=None, signals=None) -> None:
        self._template = self.read_template_file_relative_path("./vhdl/architecture.txt")
        self.instances = instances
        self.components = components
        self.signals = signals
        self.entity_name = entity_name

    def __str__(self) -> str:
        template = self._template
        template = template.replace("#ENTITY_NAME", self.entity_name)
        template = template.replace(
            "#COMPONENTS",
            self.indent(self.components, 1)
        )
        template = template.replace(
            "#INSTANCES",
            self.indent(self.instances, 1)
        )
        template = template.replace(
            "#SIGNAL_DECLARATIONS",
            self.indent(self.signals, 1)
        )
        return template
