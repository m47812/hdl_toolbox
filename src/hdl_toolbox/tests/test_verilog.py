import pytest

from ..hdl import Verilog_Module

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
    (VERILOG_TEMPLATE_STRING,
     [
        "input clk",
        "input [24:0] f_target",
        "output reg [(15*nb_input_bits)-1:0] parameter_range",
        "output signed [nb_input_bits-1:0] a_signed_signal",
        "inout some_io",
        "output [nb_input_bits-1:0] initial_phase"
    ])
])
def test_verilog_signal_extraction(source, result):
    hdl_module = Verilog_Module(source)
    assert len(result) == len(hdl_module.signals), f"Did not detect the correct amount of signals. Should: {len(result)} Was: {len(computed)}"
    for i, res in enumerate(result):
        assert hdl_module.signals[i].entity_string == res, f"Wrong signal content was \n{hdl_module.signals[i].entity_string}\n instead of:\n{res}"

@pytest.mark.parametrize("source, result", [
    (VERILOG_TEMPLATE_STRING, """module my_test_module
    #(
        parameter nb_input_bits = 2,
        parameter C_wire_p = 36'hdc413630b
    )
    (
        input clk,
        input [24:0] f_target,
        output reg [(15*nb_input_bits)-1:0] parameter_range,
        output signed [nb_input_bits-1:0] a_signed_signal,
        inout some_io,
        output [nb_input_bits-1:0] initial_phase
    );

""")
])
def test_verilog_entity_generation_test(source, result):
    HDLModule = Verilog_Module(source)
    computed = HDLModule.entity_string
    assert computed == result

@pytest.mark.parametrize("source, result", [
    (VERILOG_TEMPLATE_STRING, """my_test_module 
    #(
        .nb_input_bits(),
        .C_wire_p()
    )
inst_my_test_module
    (
        .clk(),
        .f_target(),
        .parameter_range(),
        .a_signed_signal(),
        .some_io(),
        .initial_phase()
    );
""")
])
def test_verilog_instance_generation_test(source, result):
    HDLModule = Verilog_Module(source)
    computed = HDLModule.instance_string("inst_my_test_module")
    assert computed == result