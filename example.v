/*****************************************************************************

    Example convertable SystemC header file

 *****************************************************************************/

module example (reset, clk, start, done, state, offset, target, variable);

  input          reset;
  input          clk;
  input          start;
  output         done;
  output [2:0]   state;
  input  [1:0]   offset;
  input  [7:0]   target;
  output [7:0]   variable;

  reg            done;
  reg    [2:0]   state;
  reg    [7:0]   variable;

  reg    [2:0]   next_state;
  reg            next_done;
  reg    [7:0]   next_variable;


/*****************************************************************************

    `Methods file of convertable SystemC example program

    `Author - John Hamilton

*****************************************************************************/


//`Definition of set_state method

always @(posedge clk or posedge reset)
begin
  if (reset) begin
    done <= 0;
    state <= `IDLE;
    variable <= 0;
  end else begin
    done <= next_done;
    state <= next_state;
    variable <= next_variable;
  end
end

//`Definition of get_next_state method

always @(state or start or variable or offset or target)
begin

  case (state) 

    `IDLE: begin  // Wait for start signal to occur
      if (start) begin
	next_state = `START;
	next_done = 0;
	next_variable = 0;
      end else begin
	next_state = `IDLE;
	next_done = done;
	next_variable = variable;
      end
    end

    `START: begin  // Wait until start signal goes away
      if (start) begin
	next_state = `START;
	next_variable = variable + 1;
      end else begin
	next_state = `STEP1;
	next_variable = variable;
      end
      next_done = done;
    end

    `STEP1: begin  // First step in processing something
      next_state = `STEP2;
      next_done = 0;
      next_variable = {variable[7:5],offset,variable[2:0]};
    end

    `STEP2: begin  // Next step in processing something
      if ((variable < (offset << 4)) && (offset > 1)) begin
	next_state = `STEP2;
	next_variable = variable << 1;
      end else begin
	next_state = `STEP3;
	next_variable = variable;
      end
      next_done = 0;
    end

    `STEP3: begin  // Next step in processing something
      next_state = `STEP4;
      next_done = 0;
      next_variable[3:0] = 4'hf;
      next_variable[7:4] = variable[7:4];
    end

    `STEP4: begin  // Next step in processing something
      if (variable < offset * 24) begin
	next_state = `STEP4;
	next_variable = variable + 1;
      end else begin
	next_state = `DONE;
	next_variable = variable;
      end
      next_done = 0;
    end

    `DONE: begin  // Finish up and go back to IDLE
      next_state = `IDLE;
      next_done = 1;
      next_variable = variable;
    end

    default: begin  // `Define unused states to avoid latch generation in synthesis
      next_state = `IDLE;
      next_done = done;
      next_variable = variable;
    end
  endcase
end
endmodule
