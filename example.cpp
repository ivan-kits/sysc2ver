/*****************************************************************************

    Methods file of convertable SystemC example program

    Author - John Hamilton

*****************************************************************************/

#include "example.h"

//Definition of set_state method
void example::set_state()
{
  if (reset) {
    done = 0;
    state = IDLE;
    variable = 0;
  } else {
    done = next_done;
    state = next_state;
    variable = next_variable;
  }
}

//Definition of get_next_state method
void example::get_next_state()
{

  switch (state.read()) {

    case IDLE: // Wait for start signal to occur
      if (start) {
	next_state = START;
	next_done = 0;
	next_variable = 0;
      } else {
	next_state = IDLE;
	next_done = done;
	next_variable = variable;
      }
      break;

    case START: // Wait until start signal goes away
      if (start) {
	next_state = START;
	next_variable = variable.read() + 1;
      } else {
	next_state = STEP1;
	next_variable = variable;
      }
      next_done = done;
      break;

    case STEP1: // First step in processing something
      next_state = STEP2;
      next_done = 0;
      next_variable = (variable.read().range(7,5),offset,variable.read().range(2,0));
      break;

    case STEP2: // Next step in processing something
      if ((variable.read() < (offset.read() << 4)) && (offset.read() > 1)) {
	next_state = STEP2;
	next_variable = variable.read() << 1;
      } else {
	next_state = STEP3;
	next_variable = variable;
      }
      next_done = 0;
      break;

    case STEP3: // Next step in processing something
      next_state = STEP4;
      next_done = 0;
      next_variable.range(3,0) = 0xf;
      next_variable.range(7,4) = variable.read().range(7,4);
      break;

    case STEP4: // Next step in processing something
      if (variable.read() < offset.read() * 24) {
	next_state = STEP4;
	next_variable = variable.read() + 1;
      } else {
	next_state = DONE;
	next_variable = variable;
      }
      next_done = 0;
      break;

    case DONE: // Finish up and go back to IDLE
      next_state = IDLE;
      next_done = 1;
      next_variable = variable;
      break;

    default:  // Define unused states to avoid latch generation in synthesis
      next_state = IDLE;
      next_done = done;
      next_variable = variable;
      break;
  }
}
