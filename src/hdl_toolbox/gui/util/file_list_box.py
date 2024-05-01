from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QPushButton, QWidget, QAbstractItemView

from hdl_toolbox.hdl import HDL_Module

class FileListBox(QWidget):
    def __init__(self):
        super().__init__()
        # PYQT6 code
        layout = QVBoxLayout()
        self.listbox = QListWidget()
        self.listbox.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.listbox)
        self.remove_button = QPushButton("Remove Selected File")
        self.remove_button.setStyleSheet("background-color: #807975; color: white; font-weight: bold;")
        self.remove_button.clicked.connect(self.remove_selected_file)
        layout.addWidget(self.remove_button)
        self.setLayout(layout)

        #HDL specific code
        self.hdl_modules = []

    def add_files(self, hdl_modules):
        for hdl_module in hdl_modules:
            self.listbox.addItem(hdl_module.entity_name)
            self.hdl_modules.append(hdl_module)

    def get_selected_files(self):
        selected_files = []
        for item in self.listbox.selectedItems():
            selected_files.append(self.hdl_modules[self.listbox.row(item)])
        return selected_files

    def remove_selected_file(self):
        for item in self.listbox.selectedItems():
            self.listbox.takeItem(self.listbox.row(item))
            self.hdl_modules.pop(self.listbox.row(item))
