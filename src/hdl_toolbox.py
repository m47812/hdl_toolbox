import click
from colorama import Fore

from hdl_toolbox.hdl import HDL_Module
from hdl_toolbox.util import from_file, print_title, print_filename
from hdl_toolbox.app import TopLevelCreator, VHDLDontTouchTopLevelCreator

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
        print(hdl_module.component_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def entity(files):
    for i, file in enumerate(files):
        print_title(f"Printing Entity Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        print(hdl_module.entity_string)

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def instance(files):
    for i, file in enumerate(files):
        print_title(f"Printing Instance Declarations ({i+1}/{len(files)})")
        print_filename(file)
        hdl_module = from_file(file)
        print(hdl_module.instance_string())

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('-t','--topentity', default=None, type=click.Path())
def toplevel(files, topentity):
    hdl_modules = [from_file(file) for file in files]
    if topentity is not None:
        toplevel_entity = from_file(topentity)
    else:
        toplevel_entity = None
    creator = TopLevelCreator(hdl_modules, toplevel_entity=toplevel_entity)
    creator.execute()
    print_title("Printing Top Level")
    print("\n" + creator.generate_architecture() + "\n")

@main.command()
@click.argument('files', nargs=-1, type=click.Path())
def dtt(files):
    """Prints a Dont_Touch top level file for the given entity to perform standalone synthesis (not connecting the entity) on Xilinx Devices"""
    hdl_modules = [from_file(file) for file in files]
    creator = VHDLDontTouchTopLevelCreator(hdl_modules)
    print_title("Printing Dont Touch Synthesis Top Level")
    print("\n" + str(creator) + "\n")

if __name__ == '__main__':
    main()