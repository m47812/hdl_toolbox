import pytest

from .test_vhdl import VHDL_TEMPLATE_STRING
from ..app.dont_touch_top_level import VHDLDontTouchTopLevelCreator
from ..hdl import VHDL_Module

@pytest.mark.parametrize("source, result", [
    (VHDL_TEMPLATE_STRING,
     """entity top_level_dts is

end entity top_level_dts;

architecture rtl of top_level_dts is
-- Component Declarations
    component output_position is
        generic(
            g_std_vec_size : natural := 11
        );
        port(
            clk : in std_logic;
            rst : in std_logic;
            coord_x : in std_ulogic_vector((g_std_vec_size - 1) downto 0);
            coord_y : in integer range 0 to g_std_vec_size - 1;
            coord_valid : in std_ulogic;
            threshold : out std_ulogic_vector(7 downto 0)
        );
    end component output_position;


-- Signal Declarations
    constant g_std_vec_size : natural := 11;
    signal clk : std_logic;
    signal rst : std_logic;
    signal coord_x : std_ulogic_vector((g_std_vec_size - 1) downto 0);
    signal coord_y : integer range 0 to g_std_vec_size - 1;
    signal coord_valid : std_ulogic;
    signal threshold : std_ulogic_vector(7 downto 0);


    attribute dont_touch : string;
    attribute dont_touch of inst_output_position : label is "true";
begin

    inst_output_position : component output_position
        generic map(
            g_std_vec_size => g_std_vec_size
        )
        port map(
            clk => clk,
            rst => rst,
            coord_x => coord_x,
            coord_y => coord_y,
            coord_valid => coord_valid,
            threshold => threshold
        );



end architecture rtl;""")
])
def test_dont_touch_synthesis_top(source, result):
    HDLModule = VHDL_Module(source)
    creator = VHDLDontTouchTopLevelCreator([HDLModule])
    generated_result = str(creator)
    assert generated_result == result