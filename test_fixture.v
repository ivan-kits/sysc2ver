/************************************************************************

  Test fixture RTL file

  This file is an example of a verilog test fixture file that is used
  to generate the reset and start signals. It also has the commands
  necessary to create a vcd file for viewing in gtkwave. This file
  includes the example.v file that was automatically by sysc2ver.py.

*************************************************************************/
`include "vdefs.v"

module test ();

//Signal declarations
reg	    reset;
reg	    clk;
reg	    start;
reg [1:0]   offset;
reg [7:0]   target;

wire	    done;
wire [2:0]  state;
wire [7:0]  variable;

initial
  begin
    $monitor ( $time, " ", clk, reset, start, done, state, offset, target, variable);
    $dumpfile ( "verilog.vcd" );
    $dumpvars ( 1, clk, reset, start, done, state, offset, target, variable);
    reset = 1;
    start = 0;
    offset = 2;
    target = 120;
    @(posedge clk) reset = 0;
    @(posedge clk) start = 1;
    @(posedge clk);
    @(posedge clk) start = 0;
    #300000;
    $finish;
  end

always
  begin
    clk = 0;
    #15000 clk = 1;
    #15000;
  end

example example (reset, clk, start, done, state, offset, target, variable);

endmodule

`include "example.v"
