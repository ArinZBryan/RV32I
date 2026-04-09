import types::*;

module RV32I (
    input logic Clk, _Reset
);

// Instruction Decode Signals
types::instruction_t decoded_instruction;
types::raw_instruction_t raw_instruction;

// Program Counter Signals
types::word_t pc_branch_to;
types::word_t pc;

// Register File Signals
types::regref_t rs1, rs2;
types::regref_t rd;
logic wr_e;
types::word_t instr_writeback;
types::word_t regout_a, regout_b;

program_counter module_pc (
    .Clk(Clk), 
    ._Reset(Reset), 
    .PC_branch_to(pc_branch_to), 
    .PC(pc)
);

decoder module_decoder (
    .raw(raw_instruction), 
    .decoded(decoded_instruction)
);

register_file module_rf (
    .clk(Clk), 
    ._reset(_Reset), 
    .read_reg_a(rs1), 
    .read_reg_b(rs2), 
    .write_reg(rd), 
    .write_value(instr_writeback), 
    .write_enable(wr_e), 
    .a_out(regout_a), 
    .b_out(regout_b)
);

source_mux module_srcmux (
    .srcset(decoded_instruction.data_sources),
    .instr_imm(decoded_instruction.imm),
    .pc(pc),
    .reg_rs1(rs1),
    .reg_rs2(rs2),
    .a(regout_a),
    .b(regout_b)
);

endmodule
