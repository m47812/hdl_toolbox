# HDL Toolbox
The HDL Toolbox is a collection of useful functions that can help with some of the more tedious refactoring tasks when working with HDL languages (Verilog/VHDL). For example, the tool can help with converting entity/module structures into the corresponding instance structure. It also supports interface translation (of most common types) for designs that use both VHDL and Verilog.[^1]

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[![License](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](/LICENSE)

## Feature Overview
**Language Support**

[![VHDL](https://img.shields.io/badge/VHDL-Supported-brightgreen)]()
[![Verilog](https://img.shields.io/badge/Verilog-Mostly_Supported-yellow)]()[^2] 

**Features Included**
- Conversion of Verilog or VHDL module header/entity to instantiation of the module
- A top-level connector that allows clicking together top-level files
- Interface Translation VHDL <---> Verilog
- Creation of "Don't Touch" top-levels for synthesis runs of a design without needing to connect it (e.g. resource usage).
- Creation of interfaces for use with [CocoTB](https://www.cocotb.org/) making the entity signals explicitly available on the python side.
- RegEx-based parsing of Verilog/VHDL header syntax to objects and attributes (easy expandability to other hdl code generation functions)

## How to use
The toolbox can be used in three ways. See [user guide](/doc/user_guide_console.md) on how to use and detailed feature description.
- [Console based](/doc/user_guide_console.md)
- Through GUI
- As Python classes

## Usage Example
Input:
```verilog
module test
#(
parameter myParam1 = 12,
parameter myParam2 = 2
)
(
input wire clock,
input wire reset, //Comment
output wire [7:0] busOut,
inout wire someSignal //Comment
);
```
Generate Instance Output:
```verilog
test inst_test
#(
	.myParam1(),
	.myParam2()
)(
	.clock(),
	.reset(),
	.busOut(),
	.someSignal()
);
```
Generate VHDL Component:
```vhdl
component test is
    generic(
        myParam1 : integer := 12;
        myParam2 : integer := 2
    );
    port(
        clock : in std_logic;
        reset : in std_logic;
        busOut : out std_logic_vector(7 downto 0);
        someSignal : inout std_logic
    );
end component test;
```
Generate VHDL Instance:
```vhdl
inst_test : component test
    generic map(
        myParam1 => ,
        myParam2 => 
    )
    port map(
        clock => ,
        reset => ,
        busOut => ,
        someSignal => 
    );
```
Generate VHDL Don't Touch top-level:
```vhdl
entity top_level_dts is

end entity top_level_dts;

architecture rtl of top_level_dts is
-- Component Declarations
    component test is
        generic(
            myParam1 : integer := 12;
            myParam2 : integer := 2
        );
        port(
            clock : in std_logic;
            reset : in std_logic;
            busOut : out std_logic_vector(7 downto 0);
            someSignal : inout std_logic
        );
    end component test;


-- Signal Declarations
    constant myParam1 : integer := 12;
    constant myParam2 : integer := 2;
    signal clock : std_logic;
    signal reset : std_logic;
    signal busOut : std_logic_vector(7 downto 0);
    signal someSignal : std_logic;


    attribute dont_touch : string;
    attribute dont_touch of inst_test : label is "true";

begin

    inst_test : component test
        generic map(
            myParam1 => myParam1,
            myParam2 => myParam2
        )
        port map(
            clock => clock,
            reset => reset,
            busOut => busOut,
            someSignal => someSignal
        );
end architecture rtl;
```
Python CocoTB interface:
```python
class TEST_INTERFACE:
    def __init__(self, dut):
        self.clock = dut.clock
        self.reset = dut.reset
        self.busOut = dut.busOut
        self.someSignal = dut.someSignal

    def initalize_zeros(self):
        self.clock.value = 0
        self.reset.value = 0
```



[^1]: The HDL Toolbox is a more powerful (and better maintainable) successor of my previous tool [HDL Converter](https://github.com/m47812/HDL_Converter). I will still leave the (old) HDL converter online, but as a new user I would suggest using the HDL toolbox as it should be more stable, provides more powerful features and it will be the one I will be expanding with new features in the future. 
[^2]: Reading Verilog modules and creating instances is supported. Creating top levels can read in Verilog files (mixed with VHDL), then converts the interface to VHDL and finally generates the output product as a VHDL file.
