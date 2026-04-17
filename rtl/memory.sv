import types::word_t;
import types::byte_select_t;

module memory
#(
    parameter int MEM_SIZE_BITS=16
)
(
    input logic clock,

    input types::word_t PortA_Addr, PortB_Addr,
    input types::word_t PortA_WData, PortB_WData,
    input types::byte_select_t PortA_WriteSelect, PortB_WriteSelect,

    output types::word_t PortA_Out, PortB_Out
);

logic [7:0] memory [1 << MEM_SIZE_BITS];

logic [MEM_SIZE_BITS-1:0] PortA_Addr_Real;
assign PortA_Addr_Real = PortA_Addr[MEM_SIZE_BITS-1:0];
logic [MEM_SIZE_BITS-1:0] PortB_Addr_Real;
assign PortB_Addr_Real = PortB_Addr[MEM_SIZE_BITS-1:0];

assign PortA_Out = { memory[PortA_Addr_Real + 3], memory[PortA_Addr_Real + 2], memory[PortA_Addr_Real + 1], memory[PortA_Addr_Real]};
assign PortB_Out = { memory[PortB_Addr_Real + 3], memory[PortB_Addr_Real + 2], memory[PortB_Addr_Real + 1], memory[PortB_Addr_Real]};

always_ff @(posedge clock) begin
    if (PortA_WriteSelect[0]) memory[PortA_Addr_Real + 0] <= PortA_WData[7:0];
    if (PortA_WriteSelect[1]) memory[PortA_Addr_Real + 1] <= PortA_WData[15:8];
    if (PortA_WriteSelect[2]) memory[PortA_Addr_Real + 2] <= PortA_WData[23:16];
    if (PortA_WriteSelect[3]) memory[PortA_Addr_Real + 3] <= PortA_WData[31:24];
    
    
    if (PortB_WriteSelect[0]) memory[PortB_Addr_Real + 0] <= PortB_WData[7:0];
    if (PortB_WriteSelect[1]) memory[PortB_Addr_Real + 1] <= PortB_WData[15:8];
    if (PortB_WriteSelect[2]) memory[PortB_Addr_Real + 2] <= PortB_WData[23:16];
    if (PortB_WriteSelect[3]) memory[PortB_Addr_Real + 3] <= PortB_WData[31:24];
    
end

endmodule
