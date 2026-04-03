import types::*;

module alu(
    input types::alu_op_t op,
    input types::word_t a, b,
    output types::alu_res_t res
);

function automatic types::alu_res_t sext(types::word_t v);
    return { v[31], v };
endfunction

always_comb begin
    unique case (op)
        types::ALU_ADD: res = sext(a) + sext(b);
        types::ALU_SUB: res = sext(a) - sext(b);
        types::ALU_LSHL: res = sext(a) << sext(b); 
        types::ALU_SLT: begin 
            types::alu_res_t tmp = sext(a) - sext(b);
            res = { 32'b0, tmp[32] };
        end
        types::ALU_SLTU: begin 
            types::alu_res_t tmp = sext(a) - sext(b);
            res = { 32'b0, tmp[32] };
        end
        types::ALU_XOR: res = sext(a) ^ sext(b);
        types::ALU_LSHR: res = sext(a) >> sext(b);
        types::ALU_ASHR: res = sext(a) >>> sext(b);
        types::OR: res = sext(a) | sext(b);
        types::AND: res = sext(a) & sext(b);
    endcase;
end

endmodule
