import types::word_t;
import types::source_set_e;

module source_mux (
    input types::source_set_e Set,
    input types::word_t Imm, PC, RS1, RS2,
    output types::word_t A, B
);
    
always_comb begin
    unique case (Set)
        types::SRCSET_RS1_RS2: begin
            A = RS1; B = RS2;
        end
        types::SRCSET_RS1_IMM: begin
            A = RS1; B = Imm;
        end
        types::SRCSET_PC_IMM: begin
            A = PC; B = Imm;
        end
        default: begin
            A = '0; B = '0; //this should never happen
        end
    endcase
end

endmodule
