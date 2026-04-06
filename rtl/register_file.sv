import types::word_t;
import types::regref_t;

module register_file (
    input logic clk, _reset,
    input types::regref_t read_reg_a, read_reg_b,
    input types::regref_t write_reg,
    input types::word_t write_value,
    input logic write_enable,
    output types::word_t a_out, b_out
);

types::word_t regs [32];

always_ff @(posedge clk, negedge _reset) begin
    if (!_reset) begin
        for (int i=0; i<32; ++i)
        begin: blk_reset_regs
            regs[i] <= 0;
        end
    end else begin
        if (write_enable && write_reg != '0)
            regs[write_reg] <= write_value;
    end
end

always_comb begin
    a_out = regs[read_reg_a];
    b_out = regs[read_reg_b];
end

endmodule
