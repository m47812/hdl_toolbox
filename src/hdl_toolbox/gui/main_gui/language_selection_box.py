from PyQt6.QtWidgets import QRadioButton, QVBoxLayout, QGroupBox

class LanguageSelectionBox(QGroupBox):
    def __init__(self, update_calllback):
        super().__init__()
        self.setTitle("Select Output Language")
        layout = QVBoxLayout()
        self.rb_vhdl = QRadioButton("VHDL")
        self.rb_vhdl.setChecked(True)
        self.rb_vhdl.setToolTip("Generate VHDL code")
        self.rb_verilog = QRadioButton("Verilog")
        self.rb_verilog.setToolTip("Generate Verilog code")
        self.setToolTip("Select the output language, note only entity and instance's are currently supported for verilog.")
        self.rb_vhdl.toggled.connect(self.rb_check_changed)
        layout.addWidget(self.rb_vhdl)
        layout.addWidget(self.rb_verilog)
        self.setLayout(layout)
        self.update_calllback = update_calllback

    def rb_check_changed(self):
        if self.rb_vhdl.isChecked():
            self.update_calllback("vhdl")
        else:
            self.update_calllback("verilog")