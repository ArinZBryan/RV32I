import types::*;

module alu(
    input types::alu_op_e Op,
    input types::word_t In_A, In_B,
    output types::word_t Out
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
    unique case (Op)
        types::ALU_ADD: Out = 32'(sext(In_A) + sext(In_B));
        types::ALU_SUB: Out = 32'(sext(In_A) - sext(In_B));
        types::ALU_LSHL: Out = 32'(zext(In_A) << In_B[4:0]); 
        types::ALU_SLT: begin 
            tmp = sext(In_A) - sext(In_B);
            Out = { 31'b0, tmp[32] };
        end
        types::ALU_SLTU: begin 
            tmp = zext(In_A) - zext(In_B);
            Out = { 31'b0, tmp[32] };
        end
        types::ALU_XOR: Out = 32'(zext(In_A) ^ zext(In_B));
        types::ALU_LSHR: Out = 32'(zext(In_A) >> In_B[4:0]);
        types::ALU_ASHR: Out = 32'($signed(sext(In_A)) >>> In_B[4:0]);
        types::ALU_OR: Out = 32'(zext(In_A) | zext(In_B));
        types::ALU_AND: Out = 32'(zext(In_A) & zext(In_B));
        default: Out = 32'b0;
    endcase;
end

endmodule
