import re
from colorama import Fore

from .hdl import HDL_Module, VHDL_Module

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
    elif file_path.endswith('.v'):
        raise NotImplementedError("Verilog files are not supported yet")
    else:
        raise TypeError("Inputed File Type Invalid")
    
def print_title(title):
    print(Fore.RED + "========== "+ title +" ==========" + Fore.RESET)

def print_filename(filename):
    print("Processing File: " + Fore.GREEN + filename + Fore.RESET + "\n")