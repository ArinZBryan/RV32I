import types::word_t;

module program_counter #(
    parameter types::word_t RESET_ADDR = 'h80000000
) (
    input logic Clk, _Reset, Do_Branch,
    input types::word_t PC_branch_to,
    output types::word_t PC
);

always_ff @(posedge Clk, negedge _Reset) begin
    if (~_Reset) PC <= RESET_ADDR;
    else if (Do_Branch) PC <= PC_branch_to;
    else PC <= PC + 4;
end

endmodule
