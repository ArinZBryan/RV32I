import types::*;
module test_branch_evaluator();

types::word_t alu_result;
types::word_t pc;
types::word_t pc_next;
types::word_t instr_imm;
types::branch_op_e branch_type;
types::word_t new_pc_value;

assign pc_next = pc + 4;

branch_evaluator be(
    .alu_result(alu_result),
    .pc(pc),
    .pc_next(pc_next),
    .instr_imm(instr_imm),
    .branch_type(branch_type),
    .new_pc_value(new_pc_value)
);

endmodule
