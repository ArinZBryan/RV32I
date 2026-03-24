import types::*;

module decoder (
    input types::raw_instruction_t raw,
    output types::instruction_t decoded
);

function automatic types::instruction_t decode_r(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_R;
    res.rs1 = raw.fields.r.rs1;
    res.rs2 = raw.fields.r.rs2;
    res.rd = raw.fields.r.rd;
    res.funct3 = raw.fields.r.funct3;
    res.funct7 = raw.fields.r.funct7;
    res.imm = 32'b0;
    $display("Decoding R-type instruction");
    return res;
endfunction

function automatic types::instruction_t decode_s(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_S;
    res.rs1 = raw.fields.s.rs1;
    res.rs2 = raw.fields.s.rs2;
    res.rd = 5'b0;
    res.funct3 = raw.fields.s.funct3;
    res.funct7 = 7'b0;
    res.imm = { {20{raw.fields.s.imm_upper[6]}}, raw.fields.s.imm_upper[6:0], raw.fields.s.imm_lower[4:0] };
    $display("Decoding S-type instruction");
    return res;
endfunction

function automatic types::instruction_t decode_b(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_B;
    res.rs1 = raw.fields.b.rs1;
    res.rs2 = raw.fields.b.rs2;
    res.rd = 5'b0;
    res.funct3 = raw.fields.b.funct3;
    res.funct7 = 7'b0;
    res.imm = { {19{raw.fields.b.imm_upper[6]}}, raw.fields.b.imm_upper[6], raw.fields.b.imm_lower[0], raw.fields.b.imm_upper[5:0], raw.fields.b.imm_lower[4:1], 1'b0 };
    $display("Decoding B-type instruction");
    return res;
endfunction

function automatic types::instruction_t decode_u(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_U;
    res.rs1 = 5'b0;
    res.rs2 = 5'b0;
    res.rd = raw.fields.u.rd;
    res.funct3 = 3'b0;
    res.funct7 = 7'b0;
    res.imm = raw.fields.u.imm;
    return res;
    $display("Decoding U-type instruction");
endfunction

function automatic types::instruction_t decode_j(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_J;
    res.rs1 = 5'b0;
    res.rs2 = 5'b0;
    res.rd = raw.fields.j.rd;
    res.funct3 = 3'b0;
    res.funct7 = 7'b0;
    res.imm = { {11{raw.fields.j.imm[19]}}, raw.fields.j.imm[19], raw.fields.j.imm[7:0], raw.fields.j.imm[8], raw.fields.j.imm[18:9], 1'b0 };
    $display("Decoding J-type instruction");
    return res;
endfunction

function automatic types::instruction_t decode_invalid(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_INVALID;
    res.rs1 = 5'b0;
    res.rs2 = 5'b0;
    res.rd = 5'b0;
    res.funct3 = 3'b0;
    res.funct7 = 7'b0;
    res.imm = 32'b0;
    $display("Decoding invalid instruction");
    return res;
endfunction

function automatic types::instruction_t decode_i_csr(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_ICSR;
    res.rs1 = 5'b0;
    res.rs2 = 5'b0;
    res.rd = 5'b0;
    res.funct3 = 3'b0;
    res.funct7 = 7'b0;
    res.imm = 32'b0;
    $display("Decoding CSR instruction");
    return res;
endfunction

function automatic types::instruction_t decode_fence(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_FENCE;
    res.rs1 = 5'b0;
    res.rs2 = 5'b0;
    res.rd = 5'b0;
    res.funct3 = 3'b0;
    res.funct7 = 7'b0;
    res.imm = 32'b0;
    $display("Decoding fence instruction");
    return res;
endfunction

function automatic types::instruction_t decode_i_maths(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_IMATHS;
    res.rs1 = raw.fields.i.rs1;
    res.rs2 = 5'b0;
    res.rd = raw.fields.i.rd;
    res.funct3 = raw.fields.i.funct3;
    res.funct7 = 7'b0;
    res.imm = {{20{raw.fields.i.imm[11]}}, raw.fields.i.imm};
    $display("Decoding I-type maths instruction");
    return res;
endfunction

function automatic types::instruction_t decode_i_load(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_ILOAD;
    res.rs1 = raw.fields.i.rs1;
    res.rs2 = 5'b0;
    res.rd = raw.fields.i.rd;
    res.funct3 = raw.fields.i.funct3;
    res.funct7 = 7'b0;
    res.imm = {{20{raw.fields.i.imm[11]}}, raw.fields.i.imm};
    $display("Decoding I-type load instruction");
    return res;
endfunction

function automatic types::instruction_t decode_i_jalr(input types::raw_instruction_t raw);
    types::instruction_t res;
    res.itype = types::INSTR_TYPE_IJALR;
    res.rs1 = raw.fields.i.rs1;
    res.rs2 = 5'b0;
    res.rd = raw.fields.i.rd;
    res.funct3 = raw.fields.i.funct3;
    res.funct7 = 7'b0;
    res.imm = {{20{raw.fields.i.imm[11]}}, raw.fields.i.imm};
    $display("Decoding I-type jalr instruction");
    return res;
endfunction

always_comb begin
    unique case (raw.opcode)
        7'b0110011: decoded = decode_r(raw);
        7'b0010011: decoded = decode_i_maths(raw);
        7'b0000011: decoded = decode_i_load(raw);
        7'b0100011: decoded = decode_s(raw);
        7'b1100011: decoded = decode_b(raw);
        7'b1101111: decoded = decode_j(raw);
        7'b1100111: decoded = decode_i_jalr(raw);
        7'b0110111: decoded = decode_u(raw);
        7'b1110011: decoded = decode_i_csr(raw);    // forwards to decode_invalid
        7'b0001111: decoded = decode_fence(raw);    // forwards to decode_invalid
        default: decoded = decode_invalid(raw);
    endcase
end

endmodule
