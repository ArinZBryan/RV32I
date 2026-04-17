import types::*;
module test_source_mux ();

types::source_set_e Set;
types::word_t Imm;
types::word_t PC;
types::word_t RS1;
types::word_t RS2;
types::word_t A; 
types::word_t B;

source_mux sm(
    .Set(Set),
    .Imm(Imm),
    .PC(PC),
    .RS1(RS1),
    .RS2(RS2),
    .A(A),
    .B(B)
);

endmodule
