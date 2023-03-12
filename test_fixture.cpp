/*******************************************************************

  Test fixture - methods file

  This file is an example of a verilog test fixture that will
  generate the reset and start signals to be applied to the 
  example systemc module.

*******************************************************************/

#include "test_fixture.h"

// Definition of do_command method
void test_fixture::do_command()
{
  reset = 1;
  start = 0;
  wait(1);
  reset = 0;
  wait(1);
  start = 1;
  wait(3);
  start = 0;
}
