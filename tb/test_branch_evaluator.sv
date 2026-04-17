import types::*;
module test_branch_evaluator();

types::word_t Var;
types::word_t PC_Cur;
types::word_t PC_Next;
types::word_t Offset;
types::branch_op_e Type;
types::word_t PC_Result;

assign PC_Next = PC_Cur + 4;

branch_evaluator be(
    .Var(Var),
    .PC_Cur(PC_Cur),
    .PC_Next(PC_Next),
    .Offset(Offset),
    .Type(Type),
    .PC_Result(PC_Result)
);

endmodule
