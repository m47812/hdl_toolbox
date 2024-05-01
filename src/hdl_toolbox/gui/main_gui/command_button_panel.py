import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout

from .language_selection_box import LanguageSelectionBox

class CommandButtonPanel(QWidget):
    def __init__(self, entity_clicked, component_clicked, instance_clicked, dtt_clicked, toplevel_clicked, coco_clicked):
        super().__init__()
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Create buttons
        self.bt_entity = QPushButton("Entity String")
        self.bt_component = QPushButton("Component String")
        self.bt_instance = QPushButton("Instance String")
        self.bt_dtt = QPushButton("Don't Touch Top Level")
        self.bt_toplevel = QPushButton("Top Level")
        self.bt_coco = QPushButton("COCOTB Interface")
        self.language_selection_box = LanguageSelectionBox(self.language_selection_changed_callback)

        # Register callbacks
        self.bt_entity.clicked.connect(entity_clicked)
        self.bt_component.clicked.connect(component_clicked)
        self.bt_instance.clicked.connect(instance_clicked)
        self.bt_dtt.clicked.connect(dtt_clicked)
        self.bt_toplevel.clicked.connect(toplevel_clicked)
        self.bt_coco.clicked.connect(coco_clicked)

        BUTTON_STYLE_SHEET = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        QPushButton:disabled {
            background-color: lightgray;
        }
        """

        # Set button styles
        self.bt_entity.setStyleSheet(BUTTON_STYLE_SHEET)
        self.bt_component.setStyleSheet(BUTTON_STYLE_SHEET)
        self.bt_instance.setStyleSheet(BUTTON_STYLE_SHEET)
        self.bt_dtt.setStyleSheet(BUTTON_STYLE_SHEET)
        self.bt_toplevel.setStyleSheet(BUTTON_STYLE_SHEET)
        self.bt_coco.setStyleSheet(BUTTON_STYLE_SHEET)

        # Add buttons to layout
        grid_layout.addWidget(self.bt_entity, 0, 0, 1,2)
        grid_layout.addWidget(self.bt_instance, 1, 0, 1,2)
        grid_layout.addWidget(self.language_selection_box, 0, 2, 2,1)
        layout.addLayout(grid_layout)
        layout.addWidget(self.bt_component)
        layout.addWidget(self.bt_dtt)
        #layout.addWidget(bt_toplevel) # Not yet implemented
        layout.addWidget(self.bt_coco)
        self.setLayout(layout)

        self.selected_language = "vhdl"

    def language_selection_changed_callback(self, language):
        if language == "vhdl":
            self.selected_language = "vhdl"
            self.bt_dtt.setEnabled(True)
            self.bt_toplevel.setEnabled(True)
            self.bt_component.setEnabled(True)
        else:
            self.selected_language = "verilog"
            self.bt_dtt.setEnabled(False)
            self.bt_toplevel.setEnabled(False)
            self.bt_component.setEnabled(False)


