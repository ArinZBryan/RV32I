import types::word_t;
import types::source_set_e;

module source_mux (
    input types::source_set_e srcset,
    input types::word_t instr_imm, pc, reg_rs1, reg_rs2,
    output types::word_t a, b
);
    
always_comb begin
    unique case (srcset)
        types::SRCSET_RS1_RS2: begin
            a = reg_rs1; b = reg_rs2;
        end
        types::SRCSET_RS1_IMM: begin
            a = reg_rs1; b = instr_imm;
        end
        types::SRCSET_PC_IMM: begin
            a = pc; b = instr_imm;
        end
        default: begin
            a = '0; b = '0; //this should never happen
        end
    endcase
end

endmodule
