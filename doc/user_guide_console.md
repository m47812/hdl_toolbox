# HDL Toolbox: User Guide Console

This user guide provides some instructions on using the toolbox in console mode. It assumes usage in a typical Linux-based shell environment but can generally be used on any system with Python installed.

## Installation

Clone the repository and navigate to top directory.

Install requirements using
``pip install -r requirements.txt``

## How to run

To run the console version simply execute: 

``python3 <PROJECT_PATH>/src/hdl_toolbox.py``

I would recommend setting an alias for this:

``alias hdltoolbox='python3 <PROJECT_PATH>/src/hdl_toolbox.py'``

In this guide, the command ``hdltoolbox`` will be used referring to the alias above.


## Commands
This section briefly introduces all available commands and options. All example outputs will assume sourcing from the following VHDL entity:
```vhdl
entity simple_adder is
    generic(
        g_nb_bits : natural := 8
    );
    port(
        clk : in STD_LOGIC;
        a : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
        b : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
        c : out STD_LOGIC_VECTOR(g_nb_bits downto 0)
    );
end entity simple_adder;
```

### Help

``hdltoolbox --help``

Provides a list of all available functions. Additionally use ``hdltoolbox <COMMAND NAME> --help`` on any command to show help for the command specifically.

### Component

``hdltoolbox component [FILES]``

- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Generates:
 A component declaration (VHDL) of the provided input entities. Provided Verilog files are also printed as VHDL components as the concept of "component declarations" does not exist in Verilog.


### Entity

``hdltoolbox entity [OPTIONS] [FILES]``

- ``-o`` or ``--output_language``: Determines if output is printed as VHDL (``vhdl`` or ``vhd``)  or Verilog (``verilog`` or ``v``)
- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Prints entity declarations for the specified files in the desired output language. Note that the translation is only intended for common standard data types.

Example:
``hdltoolbox entity -o v simple_adder.vhd``
Prints the input VHDL entity translated to the corresponding Verilog entity (i.e. module)
```verilog
module simple_adder
    #(
        parameter g_nb_bits = 8
    )
    (
        input clk,
        input [g_nb_bits - 1:0] a,
        input [g_nb_bits - 1:0] b,
        output [g_nb_bits:0] c
    );
```
### Instance

``hdltoolbox instance [OPTIONS] [FILES]``
- ``-o`` or ``--output_language``: Determines if output is printed as VHDL (``vhdl`` or ``vhd``)  or Verilog (``verilog`` or ``v``)
- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Prints instance declarations for the specified files in the desired output language.

Example:
``hdltoolbox instance -o v simple_adder.vhd`` Prints the input VHDL entity translated to the corresponding Verilog module instance
```verilog
simple_adder 
    #(
        .g_nb_bits()
    )
inst_simple_adder
    (
        .clk(),
        .a(),
        .b(),
        .c()
    );
```

### CocoTB

``cocotb [FILES]``
- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Prints a simple CocoTB Interface that makes the names of the (top-level) signals of the entity explicit for usage in python. It also provides an "initialize zeros" method that can be called to initialize all inputs to zero often useful fo simulations to set default values.

Example: ``hdltoolbox cocotb simple_adder.vhd`
```python
class SIMPLE_ADDER_INTERFACE:
    def __init__(self, dut):
        self.clk = dut.clk
        self.a = dut.a
        self.b = dut.b
        self.c = dut.c

    def initalize_zeros(self):
        self.clk.value = 0
        self.a.value = 0
        self.b.value = 0
```

### Top Level

``hdltoolbox toplevel [OPTIONS] [FILES]``
- ``-t``, ``--topentity``: The file path to the top-level entity that shall serve as the entity for the top-level to create. If not used an empty entity is assumed.
- ``-a``, ``--auto``: Automatically connect the top-level entity to subordinate modules if the signals have the same name and direction. This is a flag option. Useful for looping trough larger buses (e.g. AXI) or auto connecting clk signals.
- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Executing this command will open a GUI window in which you can simply connect signals by clicking.
1. Click Source Signal
2. Click Destination Signal
3. Repeat 1 and 2 until all connected
4. Close window --> Prints connected top-level

Colors: Green=Currently selected source, Red=Currently selected destination, Blue=Already connected

The signal in the signal declaration will take the name of the source signal in its entity. Having multiple entity outputs with the same name can lead to conflicts and should be connected manually afterwards. In the current version, the tool has no option to delete connections. Currently, only the creation of VHDL top-level architectures is supported, you can however instantiate sub-modules written in Verilog and use them in the top-level.

Example:
``hdltoolbox toplevel -a -t simple_adder.vhd simple_adder.vhd`` Simply create a wrapper top level with the same signals and auto-connect them. After closing the GUI with no modifications it will show:
```vhdl
architecture rtl of simple_adder is
-- Component Declarations
    component simple_adder is
        generic(
            g_nb_bits : natural := 8
        );
        port(
            clk : in STD_LOGIC;
            a : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
            b : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
            c : out STD_LOGIC_VECTOR(g_nb_bits downto 0)
        );
    end component simple_adder;


-- Signal Declarations

begin

    inst_simple_adder : component simple_adder
        generic map(
            g_nb_bits => g_nb_bits
        )
        port map(
            clk => clk,
            a => a,
            b => b,
            c => c
        );



end architecture rtl;
```

### GUI
```hdltoolbox gui```

Launches the GUI version of the hdl toolbox. It can also be launched trough executing: 
```python3 <PROJECT_PATH>/src/hdl_toolbox_gui_launch.py```.

### Don't Touch Top-Level

```hdltoolbox dtt [FILES]```
- ``FILES``: Any number of VHDL and/or Verilog files (space separated)

Creates an empty top-level entity and an instance of all given files and their signals and generics. All entities will be declared with the "DONT_TOUCH" attribute. This feature is intended to perform an unconnected synthesis/implementation run of a design without the tool removing the unconnected entity. Note that this feature was developed with Xilinx Vivado toolchain in mind and will likely need modification for other vendor tools.

Example: ```hdltoolbox dtt simple_adder.vhd``` 
```vhdl
entity top_level_dts is

end entity top_level_dts;

architecture rtl of top_level_dts is
-- Component Declarations
    component simple_adder is
        generic(
            g_nb_bits : natural := 8
        );
        port(
            clk : in STD_LOGIC;
            a : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
            b : in STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
            c : out STD_LOGIC_VECTOR(g_nb_bits downto 0)
        );
    end component simple_adder;


-- Signal Declarations
    constant g_nb_bits : natural := 8;
    signal clk : STD_LOGIC;
    signal a : STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
    signal b : STD_LOGIC_VECTOR(g_nb_bits - 1 downto 0);
    signal c : STD_LOGIC_VECTOR(g_nb_bits downto 0);


    attribute dont_touch : string;
    attribute dont_touch of inst_simple_adder : label is "true";

begin

    inst_simple_adder : component simple_adder
        generic map(
            g_nb_bits => g_nb_bits
        )
        port map(
            clk => clk,
            a => a,
            b => b,
            c => c
        );

end architecture rtl;
```
