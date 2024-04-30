from .template_manager import TemplateManager

class VerilogEntityTemplate(TemplateManager):
    def __init__(self, entity_name = None, port_signals = None, generic_signals = None) -> None:
        self._template = self.read_template_file_relative_path("./verilog/entity.txt")
        self._port_template = self.read_template_file_relative_path("./verilog/entity_port.txt")
        self._generics_template = self.read_template_file_relative_path("./verilog/entity_generics.txt")
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
    
class VerilogInstanceTemplate(VerilogEntityTemplate):
    def __init__(self, instance_name,  entity_name, port_signals = None, generic_signals = None) -> None:
        super().__init__(entity_name, port_signals, generic_signals)
        self._template = self.read_template_file_relative_path("./verilog/instance.txt")
        self._generics_template = self.read_template_file_relative_path("./verilog/instance_generics.txt")
        self.instance_name = instance_name

    def __str__(self):
        string = super(VerilogInstanceTemplate, self).__str__() 
        return string.replace("#INSTANCE_NAME", self.instance_name)