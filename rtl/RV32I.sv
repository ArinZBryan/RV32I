import types::*;

module RV32I (
    input logic Clk, _Reset
);

// Instruction Decode Signals
types::instruction_t decoded_instruction;
types::raw_instruction_t raw_instruction;

// Program Counter Signals
logic do_branch;
types::word_t pc_branch_to;
types::word_t pc;

program_counter module_pc (.Clk(Clk), ._Reset(Reset), .Do_Branch(do_branch), .PC_branch_to(pc_branch_to), .PC(PC));
decoder module_decoder (.raw(raw_instruction), .decoded(decoded_instruction));

endmodule;
