import types::*;

module result_mux(
    /* Instruction Decoded Fields*/
    input types::result_route_e Route,
    input types::mem_access_size_e Mem_Access_Size,

    /* Data Sources*/
    input types::word_t Res_ALU, PC_Next, RS2, Mem_RData,

    /* Memory Interfaces*/
    output types::byte_select_t Mem_ByteSelect,
    output types::word_t Mem_Addr, Mem_WData,

    /* Register Writeback Output*/
    output types::word_t Writeback,
    output logic Writeback_Enable
);

always_comb begin
    unique case (Route)
        types::RROUTE_ALU_RD: begin
            Mem_ByteSelect = 4'b0000;
            Mem_Addr = 0;
            Mem_WData = 0;
            Writeback = Res_ALU;
            Writeback_Enable = 1;
        end
        types::RROUTE_ALU_MEMWRITE: begin
            unique case (Mem_Access_Size)
                types::MEMSIZE_NONE: Mem_ByteSelect = 4'b0000;
                types::MEMSIZE_S8:   Mem_ByteSelect = 4'b0001;
                types::MEMSIZE_S16:  Mem_ByteSelect = 4'b0011;
                types::MEMSIZE_S32:  Mem_ByteSelect = 4'b1111;
                types::MEMSIZE_U8:   Mem_ByteSelect = 4'b0001;
                types::MEMSIZE_U16:  Mem_ByteSelect = 4'b0011;
                default: Mem_ByteSelect = 4'b0000;
            endcase
            Mem_Addr = Res_ALU;
            Mem_WData = RS2;
            Writeback = 0;
            Writeback_Enable = 0;
        end
        types::RROUTE_ALU_MEMREAD_RD: begin
            Mem_ByteSelect = 4'b0000;
            Mem_Addr = Res_ALU;
            Mem_WData = 0;
            unique case (Mem_Access_Size)
                types::MEMSIZE_NONE: Writeback = 0;
                types::MEMSIZE_S8:  Writeback = { {24{Mem_RData[7]}}, Mem_RData[7:0] };
                types::MEMSIZE_S16: Writeback = { {16{Mem_RData[15]}}, Mem_RData[15:0] };
                types::MEMSIZE_S32: Writeback = Mem_RData;
                types::MEMSIZE_U8:  Writeback = { 24'b0, Mem_RData[7:0] };
                types::MEMSIZE_U16: Writeback = { 16'b0, Mem_RData[15:0] };
                default: Writeback = 0;
            endcase
            Writeback_Enable = 1;
        end
        types::RROUTE_PC_RD: begin
            Mem_ByteSelect = 4'b0000;
            Mem_Addr = 0;
            Mem_WData = 0;
            Writeback = PC_Next;
            Writeback_Enable = 1;
        end
        default: begin
            Mem_ByteSelect = 4'b0000;
            Mem_Addr = 0;
            Mem_WData = 0;
            Writeback = 0;
            Writeback_Enable = 0;
        end
    endcase
end


endmodule
