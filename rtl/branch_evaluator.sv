import types::*;

module branch_evaluator(
    input types::word_t alu_result,
    input types::word_t pc, pc_next,
    input types::word_t instr_imm,
    input types::branch_op_e branch_type,
    output types::word_t new_pc_value
);

always_comb begin
    unique case (branch_type)
        BRANCH_NOBRANCH: new_pc_value = pc_next;
        BRANCH_OFFSET_ZERO: new_pc_value = (alu_result == '0) ? pc + instr_imm : pc_next;
        BRANCH_OFFSET_NZERO: new_pc_value = (alu_result != '0) ? pc + instr_imm : pc_next;
        BRANCH_ALU: new_pc_value = alu_result;
        default: new_pc_value = pc;
    endcase
end

endmodule
