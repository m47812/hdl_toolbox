import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QGroupBox, QCheckBox
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDrag
from PyQt6.QtCore import QEvent, Qt

from .language_selection_box import LanguageSelectionBox

from hdl_toolbox.util import from_file

class DroppablePushButton(QPushButton):
    def __init__(self, parent, style, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.parent = parent
        self._text = args[0]
        self.default_text = args[0]
        self._style = style
        self.clicked.connect(self.clickEvent)
        self.setToolTip("Select the modules to instantiate in the list above. If you additionally want to specify a top level entity, drag it on to this field")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.setText(value)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def enterEvent(self, event):
        if self.text != self.default_text:
            self.setStyleSheet("background-color: #d10808;")
            self.setText("Clear")
            event.accept()

    def clickEvent(self) -> None:
        self.text = self.default_text
        self.parent.selected_top_level = None

    def leaveEvent(self, event) -> None:
        self.setStyleSheet(self._style)
        self.setText(self.text)
        event.accept()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            selected_top_level = from_file(files[0])
        elif event.mimeData().hasText():
            selected_top_level = self.parent.get_module_callback(int(event.mimeData().text()))
        else:
            return
        self.text = "Top Level:  " + selected_top_level.entity_name
        self.parent.selected_top_level = selected_top_level
        event.acceptProposedAction()

class CommandButtonPanel(QWidget):
    def __init__(self, entity_clicked, component_clicked, instance_clicked, dtt_clicked, toplevel_clicked, coco_clicked, get_module_callback):
        super().__init__()
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        top_level_creator_grid = QGridLayout()

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

        # Create buttons
        self.bt_entity = QPushButton("Entity String")
        self.bt_component = QPushButton("Component String")
        self.bt_instance = QPushButton("Instance String")
        self.bt_dtt = QPushButton("Don't Touch Top Level")
        self.bt_toplevel = QPushButton("Create Top Level")
        self.cb_toplevel_auto_connect = QCheckBox("Auto Connect")
        self.cb_toplevel_auto_connect.setChecked(True)
        self.cb_toplevel_auto_connect.setToolTip("Automatically connect the top level entity to subordinate modules if the signals have the same name and direction")
        self.gb_toplevel = QGroupBox("Top Level Connector")
        self.bt_toplevel.setToolTip("Select the modules to instantiate in the list above. If you additionally want to specify a top level entity, drag on to the field on the left.")
        self.bt_coco = QPushButton("COCOTB Interface")
        self.language_selection_box = LanguageSelectionBox(self.language_selection_changed_callback)
        self.bt_top_level_etity = DroppablePushButton(self, """""", "<Drag top entity here>")

        # Register callbacks
        self.bt_entity.clicked.connect(entity_clicked)
        self.bt_component.clicked.connect(component_clicked)
        self.bt_instance.clicked.connect(instance_clicked)
        self.bt_dtt.clicked.connect(dtt_clicked)
        self.bt_toplevel.clicked.connect(self.top_level_creator_clicked)
        self.bt_coco.clicked.connect(coco_clicked)

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
        layout.addWidget(self.bt_coco)
        top_level_creator_grid.addWidget(self.bt_top_level_etity, 0, 0, 0, 2)
        top_level_creator_grid.addWidget(self.bt_toplevel, 0, 2, 0, 2)
        top_level_creator_grid.addWidget(self.cb_toplevel_auto_connect, 0, 4, 0, 1)
        self.gb_toplevel.setLayout(top_level_creator_grid)
        layout.addWidget(self.gb_toplevel)
        self.setLayout(layout)

        self.selected_language = "vhdl"
        self.selected_top_level = None
        self.top_level_clicked_callback = toplevel_clicked
        self.get_module_callback = get_module_callback

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

    def top_level_creator_clicked(self):
        self.top_level_clicked_callback(self.selected_top_level, self.cb_toplevel_auto_connect.isChecked())


