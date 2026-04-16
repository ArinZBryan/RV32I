import types::word_t;

module test_program_counter ();

logic Clk;
logic Reset;
types::word_t PC_branch_to;
types::word_t PC;
types::word_t PC_next;

program_counter #(.RESET_ADDR('0)) pc(
    .Clk(Clk), 
    ._Reset(Reset), 
    .PC_branch_to(PC_branch_to), 
    .PC(PC), 
    .PC_next(PC_next)
);

endmodule;
