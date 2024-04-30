from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from hdl_toolbox.util import from_file

class DragAndDropBox(QWidget):
    def __init__(self, files_added_callback=None):
        super().__init__()
        layout = QVBoxLayout()  # Create a QVBoxLayout
        self.label = QLabel("Drag and drop files here", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(50, 50, 300, 200)
        layout.addWidget(self.label)  # Add the label to the layout
        self.setLayout(layout)  # Set the layout of the widget
        self.setAcceptDrops(True)
        self.set_hover_style(False)
        self.files_added_callback = files_added_callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.set_hover_style(True)

    def dragLeaveEvent(self, event):
        self.set_hover_style(False)

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.process_files(files)
        self.set_hover_style(False)

    def process_files(self, files):
        if self.files_added_callback:
            hdl_modules = []
            for file in files:
                try:
                    hdl_modules.append(from_file(file))
                except Exception as e:
                    print(f"Failed to parse file {file}: {e}")
            self.files_added_callback(hdl_modules)

    def set_hover_style(self, is_hovered):
        palette = self.label.palette()
        if is_hovered:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("green"))
            palette.setColor(QPalette.ColorRole.Window, QColor("lightgreen"))
        else:
            palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
            palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.label.setPalette(palette)
        # Apply stylesheet for a more beautiful appearance
        if is_hovered:
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QLabel {
                    background-color: #e0e0e0;
                    border: 2px dashed green;
                    border-radius: 10px;
                    padding: 20px;
                    font-size: 16px;
                }
                """
            )
        else:
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QLabel {
                    background-color: #e0e0e0;
                    border: 2px dashed gray;
                    border-radius: 10px;
                    padding: 20px;
                    font-size: 16px;
                }
                """
            )