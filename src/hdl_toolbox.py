import click
from colorama import Fore

from hdl_toolbox.hdl import HDL_Module
from hdl_toolbox.util import from_file, print_title, print_filename, language_convert

@click.group()
def main():
    pass

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def component(files):
    for i, file in enumerate(files):
        print_title(f"Printing Component Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        hdl_module = language_convert(hdl_module, 'vhdl') #Components are only existent in VHDL
        print(hdl_module.component_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-o', '--output_language', type=click.Choice(['vhdl', 'vhd', 'verilog', 'v'], case_sensitive=False))
def entity(files, output_language):
    for i, file in enumerate(files):
        print_title(f"Printing Entity Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
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
def cocotb(files):
    for i, file in enumerate(files):
        print_title(f"Printing CocoTB Interface ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        print(hdl_module.cocotb_interface_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-t','--topentity', default=None, type=click.Path())
def toplevel(files, topentity):
    from hdl_toolbox.app.top_level_creator import TopLevelCreator
    hdl_modules = [language_convert(from_file(file), 'vhdl') for file in files]
    if topentity is not None:
        toplevel_entity = language_convert(from_file(topentity), 'vhdl')
    else:
        toplevel_entity = None
    creator = TopLevelCreator(hdl_modules, toplevel_entity=toplevel_entity)
    creator.execute()
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