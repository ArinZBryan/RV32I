import types::*;

module decoder (
    input types::raw_instruction_t Raw,
    output types::instruction_t Decoded
);

function automatic types::instruction_t decode_r(types::raw_instruction_t raw);
    types::instruction_t res;
    case (raw.fields.r.funct3)
        3'h0: 
            if (raw.fields.r.funct7 == 7'h20) res.alu_operation = types::ALU_SUB;
            else res.alu_operation = types::ALU_ADD;
        3'h5:
            if (raw.fields.r.funct7 == 7'h20) res.alu_operation = types::ALU_ASHR;
            else res.alu_operation = types::ALU_LSHR;
        default: res.alu_operation = alu_op_e'({ 1'b0, raw.fields.r.funct3 });
    endcase
    
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_RD;
    res.data_sources = types::SRCSET_RS1_RS2;
    res.rd = raw.fields.r.rd;
    res.imm = 32'b0;
    res.rs2 = raw.fields.r.rs2;
    res.rs1 = raw.fields.r.rs1;
    return res;
endfunction

function automatic types::instruction_t decode_i_maths(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_RD;
    res.alu_operation = alu_op_e'({ (raw.fields.i.imm[11:5] == 7'h20 && raw.fields.i.funct3 == 3'h5), raw.fields.i.funct3 });
    res.data_sources = types::SRCSET_RS1_IMM;
    res.rd = raw.fields.i.rd;
    if (raw.fields.i.funct3 == 3'h5) res.imm = { {27{raw.fields.i.imm[4]}}, raw.fields.i.imm[4:0] };
    else res.imm = { {20{raw.fields.i.imm[11]}}, raw.fields.i.imm };
    res.rs2 = 0;
    res.rs1 = raw.fields.i.rs1;
    return res;
endfunction

function automatic types::instruction_t decode_i_load(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::mem_access_size_e'(raw.fields.i.funct3);
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_MEMREAD_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_RS1_IMM;
    res.rd = raw.fields.i.rd;
    res.imm = { {20{raw.fields.i.imm[11]}}, raw.fields.i.imm};
    res.rs2 = 0;
    res.rs1 = raw.fields.i.rs1;
    return res;
endfunction

function automatic types::instruction_t decode_s(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::mem_access_size_e'(raw.fields.s.funct3);
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_MEMWRITE;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_RS1_IMM;
    res.rd = 0;
    res.imm = { {20{raw.fields.s.imm_upper[6]}}, raw.fields.s.imm_upper, raw.fields.s.imm_lower};
    res.rs2 = raw.fields.s.rs2;
    res.rs1 = raw.fields.s.rs1;
    return res;
endfunction

function automatic types::instruction_t decode_b(types::raw_instruction_t raw);
    types::instruction_t res;
    types::alu_op_e aluop;
    types::branch_op_e braop;
    case (raw.fields.b.funct3)
        0: begin aluop = types::ALU_XOR; braop = types::BRANCH_OFFSET_ZERO; end
        1: begin aluop = types::ALU_XOR; braop = types::BRANCH_OFFSET_NZERO; end
        4: begin aluop = types::ALU_SLT; braop = types::BRANCH_OFFSET_NZERO; end
        5: begin aluop = types::ALU_SLT; braop = types::BRANCH_OFFSET_ZERO; end
        6: begin aluop = types::ALU_SLTU; braop = types::BRANCH_OFFSET_NZERO; end
        7: begin aluop = types::ALU_SLTU; braop = types::BRANCH_OFFSET_ZERO; end
        default: begin aluop = types::ALU_ADD; braop = types::BRANCH_NOBRANCH; end// If we've not got a reaonable comparison, default to noop
    endcase
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = braop;
    res.result_route = types::RROUTE_ALU_RD;
    res.alu_operation = aluop;
    res.data_sources = types::SRCSET_RS1_RS2;
    res.rd = 0;
    res.imm = { {19{raw.fields.b.imm_upper[6]}}, raw.fields.b.imm_upper[6], raw.fields.b.imm_lower[0], raw.fields.b.imm_upper[5:0], raw.fields.b.imm_lower[4:1], 1'b0 };
    res.rs2 = raw.fields.b.rs2;
    res.rs1 = raw.fields.b.rs1;
    return res;
endfunction

function automatic types::instruction_t decode_j(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_ALU;
    res.result_route = types::RROUTE_PC_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_PC_IMM;
    res.rd = raw.fields.j.rd;
    res.imm = { {11{raw.fields.j.imm[19]}}, raw.fields.j.imm[19], raw.fields.j.imm[7:0], raw.fields.j.imm[8], raw.fields.j.imm[18:9], 1'b0 };
    res.rs2 = '0;
    res.rs1 = '0;
    return res;
endfunction

function automatic types::instruction_t decode_i_jalr(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_ALU;
    res.result_route = types::RROUTE_PC_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_RS1_IMM;
    res.rd = raw.fields.i.rd;
    res.imm = { {20{raw.fields.i.imm[11]}}, raw.fields.i.imm};
    res.rs2 = 5'b0;
    res.rs1 = raw.fields.i.rs1;
    return res;
endfunction
    
function automatic types::instruction_t decode_u_lui(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_RS1_IMM;
    res.rd = raw.fields.u.rd;
    res.imm = { raw.fields.u.imm, 12'b0 };
    res.rs2 = 5'b0;
    res.rs1 = 5'b0;
    return res;
endfunction

function automatic types::instruction_t decode_u_auipc(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_PC_IMM;
    res.rd = raw.fields.u.rd;
    res.imm = { raw.fields.u.imm, 12'b0 };
    res.rs2 = 5'b0;
    res.rs1 = 5'b0;
    return res;
endfunction

function automatic types::instruction_t decode_invalid(types::raw_instruction_t raw);
    types::instruction_t res;
    res.mem_acc_size = types::MEMSIZE_NONE;
    res.branch_operation = types::BRANCH_NOBRANCH;
    res.result_route = types::RROUTE_ALU_RD;
    res.alu_operation = types::ALU_ADD;
    res.data_sources = types::SRCSET_RS1_RS2;
    res.rd = 5'b0;
    res.imm = 32'b0;
    res.rs2 = 5'b0;
    res.rs1 = 5'b0;
    return res;
endfunction

function automatic types::instruction_t decode_i_csr(types::raw_instruction_t raw);
    if (raw.fields.i.imm == 1) $finish;
    return decode_invalid(raw);
endfunction

function automatic types::instruction_t decode_fence(types::raw_instruction_t raw);
    return decode_invalid(raw);
endfunction

always_comb begin
    unique case (Raw.opcode)
        7'b0110011: Decoded = decode_r(Raw);
        7'b0010011: Decoded = decode_i_maths(Raw);
        7'b0000011: Decoded = decode_i_load(Raw);
        7'b0100011: Decoded = decode_s(Raw);
        7'b1100011: Decoded = decode_b(Raw);
        7'b1101111: Decoded = decode_j(Raw);
        7'b1100111: Decoded = decode_i_jalr(Raw);
        7'b0110111: Decoded = decode_u_lui(Raw);
        7'b0010111: Decoded = decode_u_auipc(Raw);
        7'b1110011: Decoded = decode_i_csr(Raw);    // forwards to decode_invalid
        7'b0001111: Decoded = decode_fence(Raw);    // forwards to decode_invalid
        default: Decoded = decode_invalid(Raw);
    endcase
end

endmodule
