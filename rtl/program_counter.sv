import types::word_t;

module program_counter #(
    parameter types::word_t RESET_ADDR = 'h00000000
) (
    input logic clock, _reset,
    input types::word_t PC_New,
    output types::word_t PC_Current, PC_Next
);

assign PC_Next = PC_Current + 4;

always_ff @(posedge clock, negedge _reset) begin
    if (~_reset) PC_Current <= RESET_ADDR;
    PC_Current <= PC_New;
end

endmodule
