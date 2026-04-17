import types::*;

module RV32I (
    input logic clock, _reset
);

/* Module Output Variables */

// Decoder
types::instruction_t Decoded_Instruction;

// Register File
types::word_t Reg_RS1;
types::word_t Reg_RS2;

// Program Counter
types::word_t PC_Next;
types::word_t PC_Current;

// Source MUX
types::word_t Src_A;
types::word_t Src_B;

// ALU
types::word_t ALU_Out;

// Branch Evaluator
types::word_t Branch_PC_Result;

// Result MUX
types::word_t Writeback;
logic Writeback_Enable;
types::byte_select_t Mem_ByteSelect;
types::word_t Mem_WData;
types::word_t Mem_Addr;

// Memory
types::word_t PortA_Out;
types::word_t PortB_Out;

/* Module Input Variables */

// Decoder
types::raw_instruction_t Raw_Instruction; 
assign Raw_Instruction = raw_instruction_t'(PortA_Out);

// Register File
types::word_t Reg_WData; 
logic Reg_WE; 
types::regref_t Reg_WSelect;
types::regref_t Reg_Select_rs1;
types::regref_t Reg_Select_rs2;
assign Reg_WData = Writeback;
assign Reg_WE = Writeback_Enable;
assign Reg_WSelect = Decoded_Instruction.rd;
assign Reg_Select_rs1 = Decoded_Instruction.rs1;
assign Reg_Select_rs2 = Decoded_Instruction.rs2;

// Program Counter
types::word_t PC_New;
assign PC_New = Branch_PC_Result;

// Source MUX
types::word_t Src_rs1;
types::word_t Src_rs2;
types::word_t Src_Imm;
types::word_t Src_PC;
types::source_set_e Src_Set;
assign Src_rs1 = Reg_RS1;
assign Src_rs2 = Reg_RS2;
assign Src_Imm = Decoded_Instruction.imm;
assign Src_PC = PC_Current;
assign Src_Set = Decoded_Instruction.data_sources;

// ALU
types::word_t ALU_In_A;
types::word_t ALU_In_B;
types::alu_op_e ALU_Op;
assign ALU_In_A = Src_A;
assign ALU_In_B = Src_B;
assign ALU_Op = Decoded_Instruction.alu_operation;

// Branch Evaluator
types::word_t Branch_Var;
types::word_t Branch_PC_Next;
types::word_t Branch_PC_Cur;
types::word_t Branch_Offset;
types::branch_op_e Branch_Type;
assign Branch_Var = ALU_Out;
assign Branch_PC_Next = PC_Next;
assign Branch_PC_Cur = PC_Current;
assign Branch_Offset = Decoded_Instruction.imm;
assign Branch_Type = Decoded_Instruction.branch_operation;

// Result MUX
types::word_t Res_ALU;
types::word_t Res_PC_Next;
types::word_t Res_RS2;
types::word_t Mem_RData;
types::result_route_e Res_Route;
types::mem_acc_size_e Res_Mem_Access_Size;
assign Res_ALU = ALU_Out;
assign Res_PC_Next = PC_Next;
assign Res_RS2 = Reg_RS2;
assign Mem_RData = PortB_Out;
assign Res_Route = Decoded_Instruction.result_route;
assign Res_Mem_Access_Size = Decoded_Instruction.mem_acc_size;

// Memory
types::word_t PortA_Addr;
types::word_t PortA_WData;
types::byte_select_t PortA_WriteSelect;
types::word_t PortB_Addr;
types::word_t PortB_WData;
types::byte_select_t PortB_WriteSelect;
assign PortA_Addr = PC_Current;
assign PortA_WData = 0;
assign PortA_WriteSelect = 4'b1111;
assign PortB_Addr = Mem_Addr;
assign PortB_WDara = Mem_WData;
assign PortB_WriteSelect = Mem_ByteSelect;


/* Modules */
decoder module_decoder(
    .Raw(Raw_Instruction), 
    .Decoded(Decoded_Instruction)
);
register_file module_register_file(
    .clock(clock),
    ._reset(_reset), 
    .Select_rs1(Reg_Select_rs1), 
    .Select_rs2(Reg_Select_rs2), 
    .WSelect(Reg_WSelect),
    .WData(Reg_WData),
    .WE(Reg_WE),
    .Out_rs1(Reg_RS1),
    .Out_rs2(Reg_RS2)
);
program_counter module_program_counter(
    .clock(clock),
    ._reset(_reset),
    .PC_New(PC_New),
    .PC_Current(PC_Current),
    .PC_Next(PC_Next)
);
source_mux module_source_mux(
    .Set(Src_Set),
    .Imm(Src_Imm),
    .PC(Src_PC),
    .RS1(Src_rs1),
    .RS2(Src_rs2),
    .A(Src_A),
    .B(Src_B)
);
alu module_alu(
    .Op(ALU_Op),
    .In_A(ALU_In_A),
    .In_B(ALU_In_B),
    .Out(ALU_Out)
);
branch_evaluator module_branch_evaluator(
    .Var(Branch_Var),
    .PC_Cur(Branch_PC_Cur),
    .PC_Next(Branch_PC_Next),
    .Offset(Branch_Offset),
    .Type(Branch_Type),
    .PC_Result(Branch_PC_Result)
);
result_mux module_result_mux(
    .Route(Res_Route),
    .Mem_Access_Size(Mem_Access_Size),
    .Res_ALU(Res_ALU),
    .PC_Next(Res_PC_Next),
    .RS2(Res_RS2),
    .Mem_RData(Mem_RData),
    .Mem_ByteSelect(Mem_ByteSelect),
    .Mem_Addr(Mem_Addr),
    .Mem_WData(Mem_WData),
    .Writeback(Writeback),
    .Writeback_Enable(Writeback_Enable)
);
memory module_memory(
    .clock(clock),
    .PortA_Addr(PortA_Addr),
    .PortB_Addr(PortB_Addr),
    .PortA_WData(PortA_WData),
    .PortB_WData(PortB_WData),
    .PortA_WriteSelect(PortA_WriteSelect),
    .PortB_WriteSelect(PortB_WriteSelect),
    .PortA_Out(PortA_Out),
    .PortB_Out(PortB_Out)
);

endmodule
