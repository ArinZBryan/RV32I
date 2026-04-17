import types::*;

module branch_evaluator(
    input types::word_t Var,
    input types::word_t PC_Cur, PC_Next,
    input types::word_t Offset,
    input types::branch_op_e Type,
    output types::word_t PC_Result
);

always_comb begin
    unique case (Type)
        BRANCH_NOBRANCH: PC_Result = PC_Next;
        BRANCH_OFFSET_ZERO: PC_Result = (Var == '0) ? PC_Cur + Offset : PC_Next;
        BRANCH_OFFSET_NZERO: PC_Result = (Var != '0) ? PC_Cur + Offset : PC_Next;
        BRANCH_ALU: PC_Result = Var;
        default: PC_Result = PC_Cur;
    endcase
end

endmodule
