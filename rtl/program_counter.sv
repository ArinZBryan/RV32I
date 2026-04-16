import types::word_t;

module program_counter #(
    parameter types::word_t RESET_ADDR = 'h80000000
) (
    input logic Clk, _Reset,
    input types::word_t PC_branch_to,
    output types::word_t PC, PC_next
);

assign PC_next = PC + 4;

always_ff @(posedge Clk, negedge _Reset) begin
    if (~_Reset) PC <= RESET_ADDR;
    PC <= PC_branch_to;
end

endmodule
