import types::*;

module test_alu();

types::alu_op_e Op;
types::word_t Out;
types::word_t In_A;
types::word_t In_B;

alu module_alu (.Op(Op), .In_A(In_A), .In_B(In_B), .Out(Out));

endmodule
