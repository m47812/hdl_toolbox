import click
from colorama import Fore

from hdl import HDL_Module
from util import from_file, print_title, print_filename

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

if __name__ == '__main__':
    main()