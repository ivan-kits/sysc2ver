/*****************************************************************************

    Example convertable SystemC header file

 *****************************************************************************/
#include "systemc.h"
#include "vdefs.h"

SC_MODULE( example ) {
    sc_in<bool>		      reset;
    sc_in<bool>		      clk;
    sc_in<bool>		      start;
    sc_out<bool>	      done;
    sc_out<sc_uint<3> >	      state;
    sc_in<sc_uint<2> >	      offset;
    sc_in<sc_uint<8> >	      target;
    sc_out<sc_uint<8> >	      variable;

    sc_uint<3>		      next_state;
    sc_uint<1>		      next_done;
    sc_uint<8>		      next_variable;

    void set_state();       //methods implementing functionality
    void get_next_state();

    //Counstructor
    SC_CTOR( example ) {
        SC_METHOD( set_state );   //Synchronous with clock
        sensitive_pos << clk << reset;  

	SC_METHOD( get_next_state ); //Combinational
	sensitive << state << start << variable << offset << target;
    }

};
