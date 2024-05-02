import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget

from hdl_toolbox.gui.util import DragAndDropBox, FileListBox
from hdl_toolbox.gui.main_gui.command_button_panel import CommandButtonPanel
from .code_viewer import CodeViewer
from hdl_toolbox.app.top_level_creator import  TopLevelCreator
from hdl_toolbox.app.dont_touch_top_level import VHDLDontTouchTopLevelCreator
from hdl_toolbox.util import language_convert

"""Pyqt6 gui frame"""
class HDLToolboxGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HDL ToolBox GUI")
        self.setGeometry(100, 100, 500, 500)
        layout = QGridLayout()  # Change layout to QGridLayout
        self.file_list_box = FileListBox()
        self.button_panel = CommandButtonPanel(
            self.bt_entity_clicked,
            self.bt_component_clicked,
            self.bt_instance_clicked,
            self.bt_dtt_clicked,
            self.bt_toplevel_clicked,
            self.bt_coco_clicked
        )
        drag_and_drop_box = DragAndDropBox(files_added_callback=self.file_list_box.add_files)
        layout.addWidget(drag_and_drop_box, 0, 0) 
        layout.addWidget(self.file_list_box, 0, 1) 
        layout.addWidget(self.button_panel, 1, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    # Callback functions
    def bt_entity_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            converted_module = language_convert(module, self.button_panel.selected_language)
            viewer = CodeViewer(converted_module.entity_name, converted_module.entity_string, self)
            viewer.show()

    def bt_component_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            converted_module = module.to_vhdl()
            viewer = CodeViewer(converted_module.entity_name, converted_module.component_string, self)
            viewer.show()

    def bt_instance_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            converted_module = language_convert(module, self.button_panel.selected_language)
            viewer = CodeViewer(converted_module.entity_name, converted_module.instance_string(), self)
            viewer.show()

    def bt_dtt_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        converted_modules = [language_convert(module, "vhdl") for module in selected_modules]
        creator = VHDLDontTouchTopLevelCreator(converted_modules)
        viewer = CodeViewer("Don't Touch Top Level", str(creator), self)
        viewer.show()

    def bt_toplevel_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        converted_modules = [language_convert(module, "vhdl") for module in selected_modules]
        creator = TopLevelCreator(converted_modules, toplevel_entity=None)
        creator.execute_as_dialog()
        viewer = CodeViewer("Top Level", creator.generate_architecture(), self)
        viewer.show()

    def bt_coco_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            viewer = CodeViewer(module.entity_name, module.cocotb_interface_string, self)
            viewer.show()
