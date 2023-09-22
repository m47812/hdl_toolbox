from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QGroupBox, QMessageBox, QScrollArea, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSlot
import sys

class EntityPanel(QWidget):
    def __init__(self, button_clicked_callback, title, btn_strings1, btn_strings2, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        group_box = QGroupBox()
        layout = QGridLayout(group_box)
        title_label = QLabel(title)
        layout.addWidget(title_label, 0, 0, 1, 2)
        self.buttons = []
        for i, button_text in enumerate(btn_strings1):
            btn = QPushButton(button_text)
            btn.setStyleSheet("QPushButton { background-color: white; }")
            btn.clicked.connect(button_clicked_callback)
            layout.addWidget(btn, i+1, 0)
            self.buttons.append(btn)
        for i, button_text in enumerate(btn_strings2):
            btn = QPushButton(button_text)
            btn.setStyleSheet("QPushButton { background-color: white; }")
            btn.clicked.connect(button_clicked_callback)
            layout.addWidget(btn, i+1, 1)
            self.buttons.append(btn)
        self.layout().addWidget(group_box)
        group_box.setStyleSheet("QGroupBox { border: 1px solid black; }")


class TopLevelModulePanel(QScrollArea):
    def __init__(self, parent=None):
        super(TopLevelModulePanel, self).__init__(parent)
        self.clicked_buttons = []
        self.scrollContent = QWidget(self)
        self.layout = QHBoxLayout(self.scrollContent)
        self.setWidgetResizable(True)
        self.setWidget(self.scrollContent)

    def addEntityPanel(self, title, button_list1, button_list2):
        panel = EntityPanel(self.on_button_clicked, title, button_list1, button_list2)
        self.layout.addWidget(panel)

    @pyqtSlot()
    def on_button_clicked(self):
        btn = self.sender()
        self.clicked_buttons.append(btn)
        click_count = len(self.clicked_buttons)
        if click_count == 1:
            btn.setStyleSheet("QPushButton { background-color: green; }")
        elif click_count == 2:
            btn.setStyleSheet("QPushButton { background-color: red; }")
            self.show_buttons()
            self.clicked_buttons = []
        else:
            for panel in self.findChildren(EntityPanel):
                for btn in panel.findChildren(QPushButton):
                    btn.setStyleSheet("QPushButton { background-color: white; }")
            self.clicked_buttons = [btn]
            btn.setStyleSheet("QPushButton { background-color: green; }")

    def show_buttons(self):
        names = [btn.text() for btn in self.clicked_buttons]
        QMessageBox.information(self, "Info", f"You clicked: {names}")

class TopLevelModuleApplication:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)

    def top_level_connector_execute(self, main_panel : TopLevelModulePanel):
        main_panel.show()
        sys.exit(self.app.exec())
