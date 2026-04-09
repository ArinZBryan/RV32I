import types::*;

module alu(
    input types::alu_op_e op,
    input types::word_t a, b,
    output types::word_t res
);

function automatic types::alu_res_t sext(types::word_t v);
    return { v[31], v };
endfunction
function automatic types::alu_res_t zext(types::word_t v);
    return { 1'b0, v };
endfunction

types::alu_res_t tmp;


always_comb begin
    tmp = '0;
    unique case (op)
        types::ALU_ADD: res = 32'(sext(a) + sext(b));
        types::ALU_SUB: res = 32'(sext(a) - sext(b));
        types::ALU_LSHL: res = 32'(zext(a) << b[4:0]); 
        types::ALU_SLT: begin 
            tmp = sext(a) - sext(b);
            res = { 31'b0, tmp[32] };
        end
        types::ALU_SLTU: begin 
            tmp = zext(a) - zext(b);
            res = { 31'b0, tmp[32] };
        end
        types::ALU_XOR: res = 32'(zext(a) ^ zext(b));
        types::ALU_LSHR: res = 32'(zext(a) >> b[4:0]);
        types::ALU_ASHR: res = 32'($signed(sext(a)) >>> b[4:0]);
        types::ALU_OR: res = 32'(zext(a) | zext(b));
        types::ALU_AND: res = 32'(zext(a) & zext(b));
        default: res = 32'b0;
    endcase;
end

endmodule
