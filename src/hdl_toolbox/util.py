""" This file is part of the HDL Toolbox distribution (https://github.com/m47812/hdl_toolbox).
Copyright (c) 2024 Robin Müller.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>. """

import re
from colorama import Fore

from .hdl import HDL_Module, VHDL_Module, Verilog_Module

def _read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
    except:
        raise FileNotFoundError("The given file was not found:" + file_path)
    return data

def from_file(file_path) -> HDL_Module:
    file_content = _read_file(file_path)
    if file_path.endswith('.vhd'):
        return VHDL_Module(file_content)
    elif file_path.endswith('.vhdl'):
        return VHDL_Module(file_content)
    elif file_path.endswith('.v'):
        return Verilog_Module(file_content)
    else:
        raise TypeError("Inputed File Type Invalid")
    
def print_title(title):
    print(Fore.RED + "========== "+ title +" ==========" + Fore.RESET)

def print_filename(filename):
    print("Processing File: " + Fore.GREEN + filename + Fore.RESET + "\n")

def language_convert(hdl_module, output_language) -> HDL_Module:
    output_language = output_language.lower()
    if output_language == "vhdl" or output_language == "vhd":
        return hdl_module.to_vhdl()
    elif output_language == "verilog" or output_language == "v":
        return hdl_module.to_verilog()
    else:
        raise ValueError("Invalid Output Language")
    
def launch_gui():
    from .gui.main_gui.hdl_toolbox_gui import HDLToolboxGUI
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    gui = HDLToolboxGUI()
    gui.show()
    sys.exit(app.exec())