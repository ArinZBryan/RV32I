import types::*;

module test_register_file();

logic clk;
logic _reset;
types::regref_t read_reg_a;
types::regref_t read_reg_b;
types::regref_t write_reg;
types::word_t write_value;
logic write_enable;
types::word_t a_out;
types::word_t b_out;

register_file rf (
    .clk(clk),
    ._reset(_reset),
    .read_reg_a(read_reg_a),
    .read_reg_b(read_reg_b),
    .write_reg(write_reg),
    .write_value(write_value),
    .write_enable(write_enable),
    .a_out(a_out),
    .b_out(b_out)
);

endmodule
