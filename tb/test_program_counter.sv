import types::word_t;

module test_program_counter ();

logic clock;
logic _reset;
types::word_t PC_New;
types::word_t PC_Current;
types::word_t PC_Next;

program_counter #(.RESET_ADDR('0)) pc(
    .clock(clock), 
    ._reset(_reset), 
    .PC_New(PC_New), 
    .PC_Current(PC_Current), 
    .PC_Next(PC_Next)
);

endmodule;
