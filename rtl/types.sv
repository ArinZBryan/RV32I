package types;
    typedef logic [4:0] regref_t;
    typedef logic [31:0] word_t;

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
    
    typedef enum logic [3:0] {
        INSTR_TYPE_R,
        INSTR_TYPE_IMATHS,
        INSTR_TYPE_ILOAD,
        INSTR_TYPE_IJALR,
        INSTR_TYPE_ICSR,
        INSTR_TYPE_S,
        INSTR_TYPE_B,
        INSTR_TYPE_U,
        INSTR_TYPE_J,
        INSTR_TYPE_FENCE,
        INSTR_TYPE_INVALID
    } instruction_type_t;
    
    typedef struct packed {
        instruction_type_t itype;
        logic [4:0] rs1, rs2, rd;
        logic [2:0] funct3;
        logic [6:0] funct7;
        logic [31:0] imm;
    } instruction_t;

endpackage
