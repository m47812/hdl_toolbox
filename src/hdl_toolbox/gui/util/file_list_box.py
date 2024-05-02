from PyQt6.QtWidgets import QApplication, QListWidgetItem, QVBoxLayout, QListWidget, QPushButton, QWidget, QAbstractItemView
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

from hdl_toolbox.hdl import HDL_Module

class DraggableListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self._drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.currentRow()))
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)

class FileListBox(QWidget):
    def __init__(self):
        super().__init__()
        # PYQT6 code
        layout = QVBoxLayout()
        self.listbox = DraggableListWidget()
        self.listbox.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.listbox)
        self.remove_button = QPushButton("Remove Selected File")
        self.remove_button.setStyleSheet("background-color: #807975; color: white; font-weight: bold;")
        self.remove_button.clicked.connect(self.remove_selected_file)
        layout.addWidget(self.remove_button)
        self.setLayout(layout)

    def add_files(self, hdl_modules):
        for hdl_module in hdl_modules:
            item = QListWidgetItem(hdl_module.entity_name)
            item.setData(Qt.ItemDataRole.UserRole, hdl_module)
            self.listbox.addItem(item)

    def get_selected_files(self):
        selected_files = []
        for item in self.listbox.selectedItems():
            selected_files.append(item.data(Qt.ItemDataRole.UserRole))
        return selected_files
    
    def get_module_at_index(self, index):
        return self.listbox.item(index).data(Qt.ItemDataRole.UserRole)

    def remove_selected_file(self):
        for item in self.listbox.selectedItems():
            self.listbox.takeItem(self.listbox.row(item))
