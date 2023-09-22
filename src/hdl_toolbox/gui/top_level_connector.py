from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QGroupBox, QMessageBox, QScrollArea, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSlot
import sys

class SignalButton(QPushButton):
    def __init__(self, signal):
        super().__init__(signal.name)
        self.signal = signal

class EntityPanel(QWidget):
    def __init__(self, button_clicked_callback, title, input_singal_list, output_signal_list, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        group_box = QGroupBox()
        layout = QGridLayout(group_box)
        title_label = QLabel(title)
        layout.addWidget(title_label, 0, 0, 1, 2)
        self.buttons = []
        for i, signal in enumerate(input_singal_list):
            btn = SignalButton(signal)
            btn.setStyleSheet("QPushButton { background-color: white; }")
            btn.clicked.connect(button_clicked_callback)
            layout.addWidget(btn, i+1, 0)
            self.buttons.append(btn)
        for i, signal in enumerate(output_signal_list):
            btn = SignalButton(signal)
            btn.setStyleSheet("QPushButton { background-color: white; }")
            btn.clicked.connect(button_clicked_callback)
            layout.addWidget(btn, i+1, 1)
            self.buttons.append(btn)
        self.layout().addWidget(group_box)
        group_box.setStyleSheet("QGroupBox { border: 1px solid black; }")


class TopLevelModulePanel(QScrollArea):
    def __init__(self, add_connection_callback, parent=None):
        super(TopLevelModulePanel, self).__init__(parent)
        self.clicked_buttons = []
        self.scrollContent = QWidget(self)
        self.layout = QHBoxLayout(self.scrollContent)
        self.setWidgetResizable(True)
        self.setWidget(self.scrollContent)
        self.add_connection_callback = add_connection_callback

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
            self.add_connection_callback(self.clicked_buttons[0].signal, self.clicked_buttons[1].signal)
        elif click_count == 3:
            self.clicked_buttons[0].setStyleSheet("QPushButton { background-color: blue; }")
            self.clicked_buttons[1].setStyleSheet("QPushButton { background-color: blue; }")
            btn.setStyleSheet("QPushButton { background-color: green; }")
            self.clicked_buttons = [btn]

class TopLevelModuleApplication:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)

    def top_level_connector_execute(self, main_panel : TopLevelModulePanel):
        main_panel.show()
        self.app.exec()
