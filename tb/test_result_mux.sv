import types::*;
module test_result_mux ();

/* Instruction Decoded Fields*/
types::result_route_e Route;
types::mem_access_size_e Mem_Access_Size;

/* Data Sources*/
types::word_t Res_ALU;
types::word_t PC_Next;
types::word_t RS2;
types::word_t Mem_RData;

/* Memory Interfaces*/
types::byte_select_t Mem_ByteSelect;
types::word_t Mem_Addr;
types::word_t Mem_WData;

/* Register Writeback Output*/
types::word_t Writeback;
logic Writeback_Enable;

result_mux rm(
    .Route(Route),
    .Mem_Access_Size(Mem_Access_Size),
    .Res_ALU(Res_ALU),
    .PC_Next(PC_Next),
    .RS2(RS2),
    .Mem_RData(Mem_RData),
    .Mem_ByteSelect(Mem_ByteSelect),
    .Mem_Addr(Mem_Addr),
    .Mem_WData(Mem_WData),
    .Writeback(Writeback),
    .Writeback_Enable(Writeback_Enable)
);

endmodule
