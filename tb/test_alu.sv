import types::*;

module test_alu();

types::alu_op_e alu_op;
types::word_t result;
types::word_t a;
types::word_t b;

alu module_alu (.op(alu_op), .a(a), .b(b), .res(result));

endmodule
