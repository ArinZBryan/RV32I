import types::*;

module test_register_file();

logic clock;
logic _reset;
types::regref_t Select_rs1;
types::regref_t Select_rs2;
types::regref_t WSelect;
types::word_t WData;
logic WE;
types::word_t Out_rs1;
types::word_t Out_rs2;

register_file rf (
    .clock(clock),
    ._reset(_reset),
    .Select_rs1(Select_rs1),
    .Select_rs2(Select_rs2),
    .WSelect(WSelect),
    .WData(WData),
    .WE(WE),
    .Out_rs1(Out_rs1),
    .Out_rs2(Out_rs2)
);

endmodule
