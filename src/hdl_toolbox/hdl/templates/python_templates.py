""" This file is part of the HDL Toolbox distribution (https://github.com/m47812/hdl_toolbox).
Copyright (c) 2024 Robin Müller.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>. """

from .template_manager import TemplateManager

class COCOTBInterfaceTemplate(TemplateManager):
    def __init__(self, entity_name = None, port_signals = None, inputs = None):
        self._template = self.read_template_file_relative_path("./python/coco_interface_class.txt")
        self.entity_name = entity_name
        self.port_signals = port_signals
        self.inputs = inputs

    def __str__(self):
        template = self._template
        template = template.replace("#ENTITY_NAME", self.entity_name.upper() + "_INTERFACE")
        template = template.replace(
            "#SIGNALS",
            self.indent(self.port_signals, 2)
        )
        template = template.replace(
            "#INPUTS",
            self.indent(self.inputs, 2)
        )
        return template