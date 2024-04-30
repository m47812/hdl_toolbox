import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from hdl_toolbox.gui.main_gui import HDLToolboxGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HDLToolboxGUI()
    window.show()
    sys.exit(app.exec())