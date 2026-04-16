import types::*;

module result_mux(
    /* Instruction Decoded Fields*/
    input types::result_route_e rroute,
    input types::mem_access_size_e mem_access_size,

    /* Data Sources*/
    input types::word_t alu_res, pc_next, rs2, mem_portA_out,

    /* Memory Interfaces*/
    output types::byte_select_t mem_write_byte_enable,
    output types::word_t mem_address, mem_wdata,

    /* Register Writeback Output*/
    output types::word_t reg_writeback
);

always_comb begin
    unique case (rroute)
        types::RROUTE_ALU_RD: begin
            mem_write_byte_enable = 4'b0000;
            mem_address = 0;
            mem_wdata = 0;
            reg_writeback = alu_res;
        end
        types::RROUTE_ALU_MEMWRITE: begin
            unique case (mem_access_size)
                types::MEMSIZE_NONE: mem_write_byte_enable = 4'b0000;
                types::MEMSIZE_S8:   mem_write_byte_enable = 4'b0001;
                types::MEMSIZE_S16:  mem_write_byte_enable = 4'b0011;
                types::MEMSIZE_S32:  mem_write_byte_enable = 4'b1111;
                types::MEMSIZE_U8:   mem_write_byte_enable = 4'b0001;
                types::MEMSIZE_U16:  mem_write_byte_enable = 4'b0011;
                default: mem_write_byte_enable = 4'b0000;
            endcase
            mem_address = alu_res;
            mem_wdata = rs2;
            reg_writeback = 0;
        end
        types::RROUTE_ALU_MEMREAD_RD: begin
            mem_write_byte_enable = 4'b0000;
            mem_address = alu_res;
            mem_wdata = 0;
            unique case (mem_access_size)
                types::MEMSIZE_NONE: reg_writeback = 0;
                types::MEMSIZE_S8:  reg_writeback = { (24'(mem_portA_out[7])), mem_portA_out };
                types::MEMSIZE_S16: reg_writeback = { (16'(mem_portA_out[15])), mem_portA_out };
                types::MEMSIZE_S32: reg_writeback = mem_portA_out;
                types::MEMSIZE_U8:  reg_writeback = { 24'b0, mem_portA_out };
                types::MEMSIZE_U16: reg_writeback = { 16'b0, mem_portA_out };
            endcase

            reg_writeback = mem_portA_out;
        end
        types::RROUTE_PC_RD: begin
            mem_write_byte_enable = 4'b0000;
            mem_address = 0;
            mem_wdata = 0;
            reg_writeback = pc_next;
        end
    endcase
end


endmodule
