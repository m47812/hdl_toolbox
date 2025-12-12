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

import click
from colorama import Fore

from hdl_toolbox.hdl import HDL_Module
from hdl_toolbox.util import from_file, print_title, print_filename, language_convert

@click.group()
def main():
    pass

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-i', '--inv', is_flag=True, default=False, help="Prints a dummy component with inverted port directions \n in --> out,\n out --> in,\n inout --> inout")
def component(files, inv):
    for i, file in enumerate(files):
        print_title(f"Printing Component Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        if inv:
            hdl_module.invert_direction()
            hdl_module.entity_name += "_INVERTED"
        hdl_module = language_convert(hdl_module, 'vhdl') #Components are only existent in VHDL
        print(hdl_module.component_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-o', '--output_language', type=click.Choice(['vhdl', 'vhd', 'verilog', 'v'], case_sensitive=False))
@click.option('-i', '--inv', is_flag=True, default=False, help="Prints a dummy entity with inverted port directions \n in --> out,\n out --> in,\n inout --> inout")
def entity(files, output_language, inv):
    for i, file in enumerate(files):
        print_title(f"Printing Entity Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        if inv:
            hdl_module.invert_direction()
            hdl_module.entity_name += "_INVERTED"
        if output_language is not None:
            hdl_module = language_convert(hdl_module, output_language)
        print(hdl_module.entity_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-o', '--output_language', type=click.Choice(['vhdl', 'vhd', 'verilog', 'v'], case_sensitive=False))
def instance(files, output_language):
    for i, file in enumerate(files):
        print_title(f"Printing Instance Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        if output_language is not None:
            hdl_module = language_convert(hdl_module, output_language)
        print(hdl_module.instance_string())

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-o', '--output_language', type=click.Choice(['vhdl', 'vhd', 'verilog', 'v'], case_sensitive=False))
@click.option('-s', '--signals', is_flag=True, default=False, help="Prints the signals/wires declarations")
@click.option('-c', '--constants', is_flag=True, default=False, help="Prints the constants/localparam declarations")
def declarations(files, output_language, signals, constants):
    """Prints all signal/wire declarations for the provided input entity"""
    for i, file in enumerate(files):
        print_title(f"Printing Signal Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        if output_language is not None:
            hdl_module = language_convert(hdl_module, output_language)
        print(hdl_module.signal_declaration_string(en_constants=constants, en_signals=signals))

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def cocotb(files):
    for i, file in enumerate(files):
        print_title(f"Printing CocoTB Interface ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        print(hdl_module.cocotb_interface_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-t','--topentity', default=None, type=click.Path())
@click.option('-a', '--auto', is_flag=True, default=False, help="Automatically connect the top level entity to subordinate modules if the signals have the same name and direction")
def toplevel(files, topentity, auto):
    from hdl_toolbox.app.top_level_creator import TopLevelCreator
    hdl_modules = [language_convert(from_file(file), 'vhdl') for file in files]
    if topentity is not None:
        toplevel_entity = language_convert(from_file(topentity), 'vhdl')
    else:
        toplevel_entity = None
    creator = TopLevelCreator(hdl_modules, toplevel_entity=toplevel_entity)
    creator.execute(auto_connect=auto)
    print_title("Printing Top Level")
    print("\n" + creator.generate_architecture() + "\n")

@main.command()
def gui():
    from hdl_toolbox.util import launch_gui
    launch_gui()

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def dtt(files):
    """Prints a Dont_Touch top level file for the given entity to perform standalone synthesis (not connecting the entity) on Xilinx Devices"""
    from hdl_toolbox.app.dont_touch_top_level import VHDLDontTouchTopLevelCreator
    hdl_modules = [language_convert(from_file(file), 'vhdl') for file in files]
    creator = VHDLDontTouchTopLevelCreator(hdl_modules)
    print_title("Printing Dont Touch Synthesis Top Level")
    print("\n" + str(creator) + "\n")

if __name__ == '__main__':
    main()