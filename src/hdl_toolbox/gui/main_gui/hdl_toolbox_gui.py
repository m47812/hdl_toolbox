import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget

from hdl_toolbox.gui.util import DragAndDropBox
"""Pyqt6 gui frame"""
class HDLToolboxGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HDL ToolBox GUI")
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout()

        drag_and_drop_box = DragAndDropBox()
        layout.addWidget(drag_and_drop_box)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)