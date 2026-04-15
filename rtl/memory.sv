import types::word_t;
import types::byte_select_t;

module memory
#(
    parameter int MEM_SIZE_BITS=16
)
(
    input logic clk,

    input types::word_t portA_addr, portB_addr,
    input types::word_t portA_writeval, portB_writeval,
    input types::byte_select_t portA_write_enable, portB_write_enable,

    output types::word_t portA_memval, portB_memval
);

logic [7:0] memory [1 << MEM_SIZE_BITS];

logic [MEM_SIZE_BITS-1:0] portA_addr_real;
assign portA_addr_real = portA_addr[MEM_SIZE_BITS-1:0];
logic [MEM_SIZE_BITS-1:0] portB_addr_real;
assign portB_addr_real = portB_addr[MEM_SIZE_BITS-1:0];

assign portA_memval = { memory[portA_addr_real + 3], memory[portA_addr_real + 2], memory[portA_addr_real + 1], memory[portA_addr_real]};
assign portB_memval = { memory[portB_addr_real + 3], memory[portB_addr_real + 2], memory[portB_addr_real + 1], memory[portB_addr_real]};

always_ff @(posedge clk) begin
    if (portA_write_enable[0]) memory[portA_addr_real + 0] <= portA_writeval[7:0];
    if (portA_write_enable[1]) memory[portA_addr_real + 1] <= portA_writeval[15:8];
    if (portA_write_enable[2]) memory[portA_addr_real + 2] <= portA_writeval[23:16];
    if (portA_write_enable[3]) memory[portA_addr_real + 3] <= portA_writeval[31:24];
    
    
    if (portB_write_enable[0]) memory[portB_addr_real + 0] <= portB_writeval[7:0];
    if (portB_write_enable[1]) memory[portB_addr_real + 1] <= portB_writeval[15:8];
    if (portB_write_enable[2]) memory[portB_addr_real + 2] <= portB_writeval[23:16];
    if (portB_write_enable[3]) memory[portB_addr_real + 3] <= portB_writeval[31:24];
    
end

endmodule
