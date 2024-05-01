import pytest

from ..hdl import VHDL_Module, Verilog_Module
from ..hdl.signal import VHDLSignal, SignalDirection, Signal
from ..hdl.signal_types import VHDLRangeSignalType, VHDLVectorSignalType, VHDLSignalType

VHDL_TEMPLATE_STRING = \
"""library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity output_position is
    generic(
        g_std_vec_size  : natural := 11     --defined by image size
    );
    port(
        --general
        clk             : in  std_logic;
        rst             : in  std_logic;
        --input from position calculator
        coord_x         : in  std_ulogic_vector((g_std_vec_size - 1) downto 0);
        coord_valid     : in  std_ulogic;
        --Threshold
        threshold       : out std_ulogic_vector(7 downto 0)
    );
end entity output_position;

architecture RTL of output_position is
    signal s_coord_x        : std_ulogic_vector(g_std_vec_size downto 0);
    signal s_coord_y        : std_ulogic_vector(g_std_vec_size downto 0);
    signal s_coord_valid    : std_ulogic;
    signal s_avs_readdata   : std_logic_vector(31 downto 0);
    signal s_avs_read_old   : std_ulogic;
begin
    p_buffer : process(clk, rst)
    begin
        if rst = '1' then
            s_coord_x <= (others => '0');
            s_coord_y <= (others => '0');
            s_coord_valid <= '0';
        end if;
     end process;
end RTL;"""

VERILOG_TEMPLATE_STRING = \
"""// Revision 1.4.8 - Some Comment
// Revision 1.6.1 - Added Stuff
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module my_test_module
#(
    parameter nb_input_bits = 2,  //Some Comment
    parameter C_wire_p = 36'hdc413630b
)
(
    input clk, //Input clk
    input [24:0] f_target, //The target frequency
    output reg [(15*nb_input_bits)-1:0] parameter_range, //All multiples of of dphi from 1 to 15 (1 at LSB 15 at MSB) length 15*(nb_phase_bits)
    output signed [nb_input_bits-1:0] a_signed_signal,
    inout some_io,
    output [nb_input_bits-1:0] initial_phase //The Phase with which the output starts
    );
    
    //===============================================================
    // Constants
    //===============================================================   
    localparam b = 59;  //some comment
    wire [35:0] C_cool; 
    reg [60:0] mult_res; 
    wire [nb_input_bits-1:0] phase;
    
    assign C_cool = C_wire_p;
    
    always @(posedge clk)
    begin
    if(rst)
        mult_res <= 0;
    else
        mult_res <= C_dphi * f_target;
    end"""


@pytest.mark.parametrize("source, result", [
    (VHDL_TEMPLATE_STRING,
     """output_position 
    #(
        .g_std_vec_size()
    )
inst_output_position
    (
        .clk(),
        .rst(),
        .coord_x(),
        .coord_valid(),
        .threshold()
    );
""")
])
def test_vhdl_to_verilog_instance(source, result):
    vhdl_module = VHDL_Module(source)
    verilog_module = vhdl_module.to_verilog()
    computed = verilog_module.instance_string()
    assert computed == result

@pytest.mark.parametrize("source, result", [
    (VHDL_TEMPLATE_STRING,
     """module output_position
    #(
        parameter g_std_vec_size = 11
    )
    (
        input clk,
        input rst,
        input [(g_std_vec_size - 1):0] coord_x,
        input coord_valid,
        output [7:0] threshold
    );

""")
])
def test_vhdl_to_verilog_entity(source, result):
    vhdl_module = VHDL_Module(source)
    verilog_module = vhdl_module.to_verilog()
    computed = verilog_module.entity_string
    assert computed == result

@pytest.mark.parametrize("source, result", [
    (VERILOG_TEMPLATE_STRING,
     """entity my_test_module is
    generic(
        nb_input_bits : integer := 2;
        C_wire_p : integer := 36'hdc413630b
    );
    port(
        clk : in std_logic;
        f_target : in std_logic_vector(24 downto 0);
        parameter_range : out std_logic_vector((15*nb_input_bits)-1 downto 0);
        a_signed_signal : out signed(nb_input_bits-1 downto 0);
        some_io : inout std_logic;
        initial_phase : out std_logic_vector(nb_input_bits-1 downto 0)
    );
end entity my_test_module;""")
])
def test_verilog_to_vhdl_entity(source, result):
    verilog_module = Verilog_Module(source)
    vhdl_module = verilog_module.to_vhdl()
    computed = vhdl_module.entity_string
    assert computed == result

@pytest.mark.parametrize("source, result", [
    (VERILOG_TEMPLATE_STRING,
     """inst_my_test_module : component my_test_module
    generic map(
        nb_input_bits => ,
        C_wire_p => 
    )
    port map(
        clk => ,
        f_target => ,
        parameter_range => ,
        a_signed_signal => ,
        some_io => ,
        initial_phase => 
    );
""")
])
def test_verilog_to_vhdl_instance(source, result):
    verilog_module = Verilog_Module(source)
    vhdl_module = verilog_module.to_vhdl()
    computed = vhdl_module.instance_string()
    assert computed == result