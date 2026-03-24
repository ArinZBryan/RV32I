import types::word_t;

module test_program_counter ();

logic Clk;
logic Reset;
logic Do_Branch;
types::word_t PC_branch_to;
types::word_t PC;

program_counter #(.RESET_ADDR('0)) pc(.Clk(Clk), ._Reset(Reset), .Do_Branch(Do_Branch), .PC_branch_to(PC_branch_to), .PC(PC));

endmodule;
