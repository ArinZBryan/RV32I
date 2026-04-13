package types;
    typedef logic [4:0] regref_t;
    typedef logic [31:0] word_t;
    typedef logic [32:0] alu_res_t;

    typedef struct packed {
        union packed {
            struct packed {
                logic [6:0] funct7;
                logic [4:0] rs2;
                logic [4:0] rs1;
                logic [2:0] funct3;
                logic [4:0] rd;
            } r;
            struct packed {
                logic [11:0] imm;
                logic [4:0] rs1;
                logic [2:0] funct3;
                logic [4:0] rd;
            } i;
            struct packed {
                logic [6:0] imm_upper;
                logic [4:0] rs2;
                logic [4:0] rs1;
                logic [2:0] funct3;
                logic [4:0] imm_lower;
            } s;
            struct packed {
                logic [6:0] imm_upper;
                logic [4:0] rs2;
                logic [4:0] rs1;
                logic [2:0] funct3;
                logic [4:0] imm_lower;
            } b;
            struct packed {
                logic [19:0] imm;
                logic [4:0] rd;
            } u;
            struct packed {
                logic [19:0] imm;
                logic [4:0] rd;
            } j;
        } fields;
        logic [6:0] opcode;
    } raw_instruction_t;
    
    typedef enum logic[3:0] {
        ALU_ADD =  4'b0000,
        ALU_SUB =  4'b1000,
        ALU_XOR =  4'b0100,
        ALU_OR  =  4'b0110,
        ALU_AND =  4'b0111,
        ALU_LSHL = 4'b0001,
        ALU_LSHR = 4'b0101,
        ALU_ASHR = 4'b1101,
        ALU_SLT =  4'b0010,
        ALU_SLTU = 4'b0011
    } alu_op_e;

    typedef enum logic[1:0] {
        RROUTE_ALU_RD         = 0,
        RROUTE_ALU_MEMREAD_RD = 1,
        RROUTE_ALU_MEMWRITE   = 2,
        RROUTE_PC_RD_ALU_PC   = 3
    } result_route_e;

    typedef enum logic[2:0] {
        BRANCH_NOBRANCH       = 0, 
        BRANCH_OFFSET_ZERO    = 1,
        BRANCH_OFFSET_NZERO   = 2,
        BRANCH_OFFSET_ALWAYS  = 3,
        BRANCH_ABSOLUTE       = 4 
    } branch_op_e;

    typedef enum logic[1:0] {
        SRCSET_RS1_RS2 = 2'b10, 
        SRCSET_RS1_IMM = 2'b11, 
        SRCSET_PC_IMM  = 2'b01
    } source_set_e;

    typedef enum logic[2:0] {
        MEMSIZE_S8  = 3'b000,
        MEMSIZE_S16 = 3'b001,
        MEMSIZE_S32 = 3'b010,
        MEMSIZE_U8  = 3'b100,
        MEMSIZE_U16 = 3'b101,
        MEMSIZE_NONE = 3'b111
    } mem_access_size_e;

    typedef struct packed {
        mem_access_size_e mem_acc_size;
        branch_op_e branch_operation;   
        result_route_e result_route;    
        alu_op_e alu_operation;         
        source_set_e data_sources;      
        regref_t rd;                    
        word_t imm;                     
        regref_t rs2;                   
        regref_t rs1;                   
    } instruction_t;

endpackage
