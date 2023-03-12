/*****************************************************************************
 
  main.cpp -- This is the top level file instantiating the modules and
              binding ports to signals.
 
  Original Author: John Hamilton
 
 *****************************************************************************/

#include "systemc.h"
#include "vdefs.h"
#include "test_fixture.h"
#include "example.h"

int sc_main(int ac, char *av[])
{
  //Signals
  //Clock
  sc_set_time_resolution(1, SC_NS);
  sc_set_default_time_unit(1, SC_NS);
  sc_clock	    clk ("clk", 30996, 0.50, true); // 32KHz clock

  // Trace file definition
  sc_trace_file *tf = sc_create_vcd_trace_file ("systemc");

  // Command sequencer signals
  sc_signal<bool>	    reset;
  sc_signal<bool>	    start;
  sc_signal<bool>	    done;
  sc_signal<sc_uint<3> >    state;
  sc_signal<sc_uint<2> >    offset;
  sc_signal<sc_uint<8> >    target;
  sc_signal<sc_uint<8> >    variable;

  // Module instantiation
  example EXAMPLE("example");
  EXAMPLE.reset(reset);
  EXAMPLE.clk(clk);
  EXAMPLE.start(start);
  EXAMPLE.done(done);
  EXAMPLE.state(state);
  EXAMPLE.offset(offset);
  EXAMPLE.target(target);
  EXAMPLE.variable(variable);

  test_fixture FIXTURE("test_fixture");
  FIXTURE.reset(reset);
  FIXTURE.clk(clk);
  FIXTURE.start(start);

  // Trace file probes
  sc_trace(tf, reset, "reset");
  sc_trace(tf, clk, "clk");
  sc_trace(tf, start, "start");
  sc_trace(tf, done, "done");
  sc_trace(tf, state, "state");
  sc_trace(tf, offset, "offset");
  sc_trace(tf, target, "target");
  sc_trace(tf, variable, "varible");

  // Assign values, start clock and specify run time.
  offset = 2;
  target = 120;
  sc_start(clk, 600, SC_US);
  sc_close_vcd_trace_file(tf);

  return 0;
}
