import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class CommandButtonPanel(QWidget):
    def __init__(self, entity_clicked, component_clicked, instance_clicked, dtt_clicked, toplevel_clicked, coco_clicked):
        super().__init__()
        layout = QVBoxLayout()

        # Create buttons
        bt_entity = QPushButton("Entity String")
        bt_component = QPushButton("Component String")
        bt_instance = QPushButton("Instance String")
        bt_dtt = QPushButton("Don't Touch Top Level")
        bt_toplevel = QPushButton("Top Level")
        bt_coco = QPushButton("COCOTB Interface")

        # Register callbacks
        bt_entity.clicked.connect(entity_clicked)
        bt_component.clicked.connect(component_clicked)
        bt_instance.clicked.connect(instance_clicked)
        bt_dtt.clicked.connect(dtt_clicked)
        bt_toplevel.clicked.connect(toplevel_clicked)
        bt_coco.clicked.connect(coco_clicked)

        # Set button styles
        bt_entity.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        bt_component.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        bt_instance.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        bt_dtt.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        bt_toplevel.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        bt_coco.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")

        # Add buttons to layout
        layout.addWidget(bt_entity)
        layout.addWidget(bt_component)
        layout.addWidget(bt_instance)
        layout.addWidget(bt_dtt)
        #layout.addWidget(bt_toplevel) # Not yet implemented
        layout.addWidget(bt_coco)

        self.setLayout(layout)

