import types::*;
module test_source_mux ();

types::source_set_e input_srcset;
types::word_t input_instr_imm;
types::word_t input_pc;
types::word_t input_reg_rs1;
types::word_t input_reg_rs2;
types::word_t output_a; 
types::word_t output_b;

source_mux sm(
    .srcset(input_srcset),
    .instr_imm(input_instr_imm),
    .pc(input_pc),
    .reg_rs1(input_reg_rs1),
    .reg_rs2(input_reg_rs2),
    .a(output_a),
    .b(output_b)
);

endmodule
