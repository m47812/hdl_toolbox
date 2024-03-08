from .template_manager import TemplateManager

class COCOTBInterfaceTemplate(TemplateManager):
    def __init__(self, entity_name = None, port_signals = None, inputs = None):
        self._template = self.read_template_file_relative_path("./python/coco_interface_class.txt")
        self.entity_name = entity_name
        self.port_signals = port_signals
        self.inputs = inputs

    def __str__(self):
        template = self._template
        template = template.replace("#ENTITY_NAME", self.entity_name)
        template = template.replace(
            "#SIGNALS",
            self.indent(self.port_signals, 2)
        )
        template = template.replace(
            "#INPUTS",
            self.indent(self.inputs, 2)
        )
        return template