import types::word_t;
import types::regref_t;

module register_file (
    input logic clock, _reset,
    input types::regref_t Select_rs1, Select_rs2,
    input types::regref_t WSelect,
    input types::word_t WData,
    input logic WE,
    output types::word_t Out_rs1, Out_rs2
);

types::word_t regs [32];

always_ff @(posedge clock, negedge _reset) begin
    if (!_reset) begin
        for (int i=0; i<32; ++i)
        begin: blk_reset_regs
            regs[i] <= 0;
        end
    end else begin
        if (WE && WSelect != '0)
            regs[WSelect] <= WData;
    end
end

always_comb begin
    Out_rs1 = regs[Select_rs1];
    Out_rs2 = regs[Select_rs2];
end

endmodule
