import pytest

from ..hdl import VHDL_Module
from ..hdl.signal import VHDLSignal, SignalDirection, Signal
from ..hdl.signal_types import VHDLRangeSignalType, VHDLVectorSignalType, VHDLSignalType

@pytest.mark.parametrize("source, result", [
    ("""library ieee;
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
        coord_y         : in  integer range 0 to g_std_vec_size - 1;
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
end RTL;""",
     [
        "clk             : in  std_logic",
        "rst             : in  std_logic",
        "coord_x         : in  std_ulogic_vector((g_std_vec_size - 1) downto 0)",
        "coord_y         : in  integer range 0 to g_std_vec_size - 1",
        "coord_valid     : in  std_ulogic",
        "threshold       : out std_ulogic_vector(7 downto 0)"
    ])
])

def test_vhdl_signal_extraction(source, result):
    hdl_module = VHDL_Module()
    computed, _ = hdl_module._extract_signals_and_generics_strings(source)
    assert len(result) == len(computed), f"Did not detect the correct amount of signals. Should: {len(result)} Was: {len(computed)}"
    for i, res in enumerate(result):
        assert computed[i] == res, f"Wrong signal content was \n{computed[i]}\n instead of:\n{res}"


@pytest.mark.parametrize("source, ref_result",[
    ("clk             : in  std_logic", "clk : in std_logic"),
    ("coord_x    : in  std_ulogic_vector((g_std_vec_size - 1) downto 0)", "coord_x : in std_ulogic_vector((g_std_vec_size - 1) downto 0)"),
    ("coord_y    : in  integer range 0 to g_std_vec_size - 1", "coord_y : in integer range 0 to g_std_vec_size - 1"),
    ("g_std_vec_size  : natural := 11", "g_std_vec_size : natural := 11")
]
)
def test_vhdl_signal_parsing_and_string_gen(source, ref_result):
    computed = VHDLSignal(source)
    converted_back_string = computed.entity_string
    assert converted_back_string == ref_result, "Strings did not match \n Should:\n" + ref_result + "\n was:\n" + converted_back_string
