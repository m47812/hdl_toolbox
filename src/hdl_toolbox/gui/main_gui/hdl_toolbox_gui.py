import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget

from hdl_toolbox.gui.util import DragAndDropBox, FileListBox
from hdl_toolbox.gui.main_gui.command_button_panel import CommandButtonPanel
from .code_viewer import CodeViewer
from hdl_toolbox.app import VHDLDontTouchTopLevelCreator, TopLevelCreator
"""Pyqt6 gui frame"""
class HDLToolboxGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HDL ToolBox GUI")
        self.setGeometry(100, 100, 500, 500)
        layout = QGridLayout()  # Change layout to QGridLayout
        self.file_list_box = FileListBox()
        button_panel = CommandButtonPanel(
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
        layout.addWidget(button_panel, 1, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.code_viewers = []

    # Callback functions
    def bt_entity_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            viewer = CodeViewer(module.entity_name, module.entity_string)
            self.code_viewers.append(viewer)
            viewer.show()

    def bt_component_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            viewer = CodeViewer(module.entity_name, module.component_string)
            self.code_viewers.append(viewer)
            viewer.show()

    def bt_instance_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            viewer = CodeViewer(module.entity_name, module.instance_string())
            self.code_viewers.append(viewer)
            viewer.show()

    def bt_dtt_clicked(self):
        print("dtt clicked")
        selected_modules = self.file_list_box.get_selected_files()
        creator = VHDLDontTouchTopLevelCreator(selected_modules)
        viewer = CodeViewer("Don' Touch Top Level", str(creator))
        self.code_viewers.append(viewer)
        viewer.show()

    def bt_toplevel_clicked(self):
        raise NotImplementedError("Toplevel creator not implemented in GUI yet")

    def bt_coco_clicked(self):
        selected_modules = self.file_list_box.get_selected_files()
        for module in selected_modules:
            viewer = CodeViewer(module.entity_name, module.cocotb_interface_string)
            self.code_viewers.append(viewer)
            viewer.show()
