/************************************************************************

    Test fixture header file

************************************************************************/
#include "systemc.h"

SC_MODULE( test_fixture) {
    sc_out<bool>        reset;
    sc_in<bool>         clk; 
    sc_out<bool>        start;

    void do_command();

    //Counstructor
    SC_CTOR( test_fixture ) {

        SC_CTHREAD( do_command, clk.pos() );   //Declare do_command as SC_METHOD
    }

};
