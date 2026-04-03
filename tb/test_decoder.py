from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic
from cocotb.triggers import FallingEdge
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *
from aenum import IntEnum, NoAlias
from typing import Union, Iterable

class CMP_TYPE(IntEnum):
    EQ  = 0
    NEQ = 1
    LT  = 4
    GE  = 5
    LTU = 6
    GEU = 7
    
class REG(IntEnum):
    __settings__ = NoAlias
    
    zero = 0
    ra = 1
    sp = 2
    gp = 3
    tp = 4
    t0 = 5
    t1 = 6
    t2 = 7
    s0 = 8
    fp = 8
    s1 = 9
    a0 = 10
    a1 = 11
    a2 = 12
    a3 = 13
    a4 = 14
    a5 = 15
    a6 = 16
    a7 = 17
    s2 = 18
    s3 = 19
    s4 = 20
    s5 = 21
    s6 = 22
    s7 = 23
    s8 = 24
    s9 = 25
    s10 = 26
    s11 = 27
    t3 = 28
    t4 = 29
    t5 = 30
    t6 = 31

def in_unsigned_bits(value: int, bits: int) -> bool:
    """Checks if a number is a valid `bits`-bit unsigned number
    
    :param value: The number to check.
    :param bits: The number of bits `value` must fit in as an unsigned number.
    :returns: Whether the number is representable as a `bits`-bit unsigned number.
    """
    
    if value < 0:
        return False
    elif value >= 2**bits:
        return False
    else:
        return True

def in_signed_bits(value: int, bits: int) -> bool:
    """Checks if a number is a valid `bits`-bit signed number
    
    :param value: The number to check.
    :param bits: The number of bits `value` must fit in as a signed number.
    :returns: Whether the number is representable as a `bits`-bit signed number using 2's complement
    """
    
    if value < (-(2**(bits - 1))):
        return False
    elif value > (2**(bits-1) - 1):
        return False
    else:
        return True


class raw_instruction(LogicArray):
    def __init__(self, value: Union[int, str, Iterable[Union[Union[str, int, bool], "Logic"]]]):
        super().__init__(value, Range(32, 'downto', 0))
        
    @staticmethod
    def encode_r(opcode: int, rd: int | REG, funct3: int, rs1: int | REG, rs2: int | REG, funct7: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'R', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits. This should only ever be `0b0110011` as it is the same for -all R-type instructions, but other values are accepted
        :param rd: The register to place the result of the instruction into.
        :param funct3: The three bits determining which binary operation to perform
        :param rs1: The register containing the first operand.
        :param rs2: The register containing the second operand.
        :param funct7: The seven bits containing the modifier (if needed for this instruction). The only valid values are `0x0` and `0x20`, the latter of which is only valid to turn ADD into SUB and SRL into SRA.
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `rd` is not a 5-bit unsigned, `funct3` is not a 3-bit unsigned, `rs1` is not a 5-bit unsigned, `rs2` is not a 5-bit unsigned or `funct7` is not a 7-bit unsigned integer.
        """

        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(rd, 5) or
            not in_unsigned_bits(funct3, 3) or
            not in_unsigned_bits(rs1, 5) or
            not in_unsigned_bits(rs2, 5) or
            not in_unsigned_bits(funct7, 7)
        ):
            raise ValueError()
        return raw_instruction(
            (funct7 & 0b111_1111) << 25 |
            (rs2 & 0b1_1111)      << 20 |
            (rs1 & 0b1_1111)      << 15 |
            (funct3 & 0b111)      << 12 |
            (rd & 0b1_1111)       << 7  |
            (opcode & 0b111_1111)
        )        
    @staticmethod
    def encode_i(opcode: int, rd: int | REG, funct3: int, rs1: int | REG, imm: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'I', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits.
        :param rd: The register to place the result of the instruction into.
        :param funct3: The three bits determining the options for this instruction.
        :param rs1: The register containing the first operand.
        :param imm: The immediate second operand.
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `rd` is not a 5-bit unsigned, `funct3` is not a 3-bit unsigned, `rs1` is not a 5-bit unsigned, or `imm` is not a 12-bit signed integer.
        """
        
        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(rd, 5) or
            not in_unsigned_bits(funct3, 3) or
            not in_unsigned_bits(rs1, 5) or
            not in_signed_bits(imm, 12)
        ):
            raise ValueError()
        return raw_instruction(
            (imm & 0b1111_1111_1111) << 20 |
            (rs1 & 0b1_1111)         << 15 |
            (funct3 & 0b111)         << 12 |
            (rd & 0b1_1111)          << 7  |
            (opcode & 0b111_1111)
        )
    @staticmethod
    def encode_s(opcode: int, funct3: int, rs1: int | REG, rs2: int | REG, imm: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'S', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits. This should only ever be `0b0100011` as it is the same for all store instructions, but other values are accepted
        :param funct3: The 3-bits determining how much of `rs2` is stored. Only the values 0, 1 and 2 correspond to valid instructions.
        :param rs1: The register containing the base address of the storage location in memory.
        :param rs2: The register containing the item to store's bytes.
        :param imm: The immediate offset from the base address' storage location in memory.
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `funct3` is not a 3-bit unsigned, `rs1` is not a 5-bit unsigned, `rs2` is not a 5-bit unsigned or `imm` is not a 12-bit signed integer.
        """
        
        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(funct3, 3) or
            not in_unsigned_bits(rs1, 5) or
            not in_unsigned_bits(rs2, 5) or
            not in_signed_bits(imm, 12)
        ):
            raise ValueError()
        return raw_instruction(
            (imm & 0b1111_1110_0000) << 25 |
            (rs2 & 0b1_1111)         << 20 |
            (rs1 & 0b1_1111)         << 15 |
            (funct3 & 0b111)         << 12 |
            (imm & 0b0000_0001_1111) << 7  |
            (opcode & 0b111_1111)
        )
    @staticmethod
    def encode_b(opcode: int, funct3: int | CMP_TYPE , rs1: int | REG, rs2: int | REG, imm: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'B', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits. This should only ever be `0b1100011` as it is the same for all branch instructions, but other values are accepted
        :param funct3: The 3-bits determining which comparison type is performed before branching. The values 2 and 3 do not correspond to valid instructions.
        :param rs1: The register containing the first item to compare
        :param rs2: The register containing the second item to compare
        :param imm: The immediate being placed into the destination register
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `funct3` is not a 3-bit unsigned, `rs1` is not a 5-bit unsigned, `rs2` is not a 5-bit unsigned or `imm` is not an even 13-bit signed integer.
        """
        
        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(funct3, 3) or
            not in_unsigned_bits(rs1, 5) or
            not in_unsigned_bits(rs2, 5) or
            not in_signed_bits(imm, 13) or
            imm % 2 == 0
        ):
            raise ValueError()
        return raw_instruction(
            (imm & 0b1_0000_0000_0000) << 31 |
            (imm & 0b0_0111_1110_0000) << 25 |
            (rs2 & 0b1_1111)           << 20 |
            (rs1 & 0b1_1111)           << 15 |
            (funct3 & 0b111)           << 12 |
            (imm & 0b0_0000_0001_1110) << 8  |
            (imm & 0b0_1000_0000_0000) << 7  |
            (opcode & 0b111_1111)
        ) 
    @staticmethod
    def encode_u(opcode: int, rd: int | REG, imm: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'U', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits. This should only ever be `0b0110111` or `0b0010111` (LUI and AUIPC, the only valid U-type instructions in RV32I), but other values are accepted
        :param rd: The destination register of the instruction.
        :param imm: The immediate being placed into the destination register
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `rd` is not a 5-bit unsigned or imm is not a 32-bit signed integer.
        """
        
        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(rd, 5) or
            not in_signed_bits(imm, 32)
        ):
            raise ValueError()
        return raw_instruction(
            (imm & 0b1111_1111_1111_1111_1111_0000_0000_0000) << 12 |
            (rd & 0b1_1111)                                   << 7  |
            (opcode & 0b111_1111) 
        )  
    @staticmethod
    def encode_j(opcode: int, rd: int | REG, imm: int) -> "raw_instruction":
        """
        Encodes a `raw_instruction_t` of known type 'J', using python integer arguments
        
        :param opcode: The opcode that should be placed into the first seven bits. This should only ever be `0b1101111` (JALR, the only valid J-type instruction in RV32I), but other values are accepted
        :param rd: The destination register of the instruction. This is where the return address of the JALR instruction is placed.
        :param imm: The immediate value of bytes by which to jump
        :returns: A python `raw_instruction` containing the encoded instruction as a `raw_instruction_t`
        :raises ValueError: When the `opcode` is not a 7-bit unsigned, `rd` is not a 5-bit unsigned or imm is not an even 21-bit signed integer.
        """
        
        if (
            not in_unsigned_bits(opcode, 7) or
            not in_unsigned_bits(rd, 5) or
            not in_signed_bits(imm, 21) or
            imm % 2 == 1
        ):
            raise ValueError()
        return raw_instruction(
            (imm & 0b0000_0000_0001_0000_0000_0000_0000_0000) << 31 |
            (imm & 0b0000_0000_0000_0000_0000_0111_1111_1110) << 21 |
            (imm & 0b0000_0000_0000_0000_0000_1000_0000_0000) << 20 |
            (imm & 0b0000_0000_0000_1111_1111_0000_0000_0000) << 12 |
            (rd & 0b1_1111)                                   << 7  |
            (opcode & 0b111_1111) 
        )

# typdef enum logic[4:0] { ... } alu_op_t
class ALU_OPERATION(IntEnum):
    ADD =  0b0000
    SUB =  0b1000
    XOR =  0b0100
    OR  =  0b0110
    AND =  0b0111
    LSHL = 0b0001
    LSHR = 0b0101
    ASHR = 0b1101
    SLT =  0b0010
    SLTU = 0b0011
    
# typdef enum logic[1:0] { ... } res_route_t
class RESULT_ROUTE(IntEnum):
    ALU_RD = 0
    ALU_MEMREAD_RD = 1
    ALU_MEMWRITE = 2
    PC_RD_ALU_PC = 3

# typedef enum logic[2:0] { ... } bra_op_t
class BRANCH_OPERATION(IntEnum):
    NOBRANCH = 0
    OFFSET_ZERO = 1
    OFFSET_NZERO = 2
    OFFSET_ALWAYS = 3
    ABSOLUTE_ALU = 4

# typedef enum logic[1:0] { ... } src_set_t
class SOURCE_SET(IntEnum):
    RS1_RS2 = 0b01
    RS1_IMM = 0b10
    PC_IMM =  0b11
    
class instruction(LogicArray):
    def __init__(self, 
        rs1 : REG | int = REG.zero,                                     #  0 +  5 = 5
        rs2 : REG | int = REG.zero,                                     #  5 +  5 = 10
        imm : int = 0,                                                  # 10 + 32 = 42
        dst : REG | int = REG.zero,                                     # 42 +  5 = 47
        srcs : SOURCE_SET | int = SOURCE_SET.RS1_RS2,                   # 47 +  3 = 50
        alu_op : ALU_OPERATION | int = ALU_OPERATION.ADD,               # 50 +  5 = 55
        res_route : RESULT_ROUTE | int = RESULT_ROUTE.ALU_RD, # 55 +  2 = 57
        bra_op: BRANCH_OPERATION | int = BRANCH_OPERATION.NOBRANCH      # 57 +  3 = 60
    ):
        super().__init__(
            (bra_op & 0x7)     << 57 |
            (res_route & 0x3)  << 55 |
            (alu_op & 0x1f)    << 50 |
            (srcs & 0x7)       << 47 |
            (dst & 0x1f)       << 42 |
            (imm & 0xffffffff) << 10 |
            (rs2 & 0x1f)         << 5  |
            (rs1 & 0x1f), 
            Range(6, 'downto', 0))

    @property
    def rs1(self) -> REG:
        return REG(self[0:5])
    @property
    def rs2(self) -> REG:
        return REG(self[5:10])
    @property
    def imm(self) -> int:
        return int(self[10:42])
    @property
    def dst(self) -> bool:
        return bool(self[42:47])
    @property
    def srcs(self) -> SOURCE_SET:
        return SOURCE_SET(self[47:50])
    @property
    def alu_op(self) -> ALU_OPERATION:
        return ALU_OPERATION(self[50:55])
    @property
    def res_route(self) -> RESULT_ROUTE:
        return RESULT_ROUTE(self[55:57])
    @property
    def bra_op(self) -> BRANCH_OPERATION:
        return BRANCH_OPERATION(self[57:60])
    
def decode(instr: raw_instruction) -> instruction:
    """
    Simulates the expected behaviour of decoding of a `raw_instruction_t` into an `instruction_t` in python
    
    :param instruction: The `raw_instruction`
    :returns: The decoded `instruction`
    :raises ValueError: When the input `LogicArray` is the wrong size, or is not resolved. 
    """
    
    if not instr.is_resolvable or instr.range.left != 61 or instr.range.right != 0:
        raise ValueError()
    
    match int(instr[0:7]):
        case 0b0110011: # r-type
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG(int(instr[20:25])),
                imm = 0,
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_RS2,
                alu_op = ALU_OPERATION(
                    int(instr[12:15]) + 
                    (0b1000 if instr[25:32] == 0x20 else 0) # use ALU_SUB or ALU_ASHR if needed
                ),
                res_route = RESULT_ROUTE.ALU_RD,
                bra_op = BRANCH_OPERATION.NOBRANCH
            )
        case 0b0010011: # i-type maths
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG.zero,
                imm = int(instr[20:32]) if (instr[12:15] != 0x5) else int(instr[20:25]),
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_IMM,
                alu_op = ALU_OPERATION(int(instr[12:15]) + (0b1000 if (instr[25:31] == 0x20 and instr[12:15] == 0x5) else 0)),
                res_route = RESULT_ROUTE.ALU_RD,
                bra_op = BRANCH_OPERATION.NOBRANCH
            ) 
        case 0b0000011: # i-type loads
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG.zero,
                imm = int(instr[20:32]),
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_IMM,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.ALU_MEMREAD_RD,
                bra_op = BRANCH_OPERATION.NOBRANCH
            ) 
        case 0b0100011: # s-type
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG(int(instr[20:25])),
                imm = int(instr[7:12]) + (int(instr[25:32]) << 5),
                dst = REG.zero,
                srcs = SOURCE_SET.RS1_IMM,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.ALU_MEMWRITE,
                bra_op = BRANCH_OPERATION.NOBRANCH
            )
        case 0b1100011: # b-type
            aluop = ALU_OPERATION(0)
            braop = BRANCH_OPERATION(0)
            match instr[12:15]:
                case 0x0: aluop = ALU_OPERATION.XOR; braop = BRANCH_OPERATION.OFFSET_ZERO
                case 0x1: aluop = ALU_OPERATION.XOR; braop = BRANCH_OPERATION.OFFSET_NZERO
                case 0x4: aluop = ALU_OPERATION.SLT; braop = BRANCH_OPERATION.OFFSET_NZERO
                case 0x5: aluop = ALU_OPERATION.SLT; braop = BRANCH_OPERATION.OFFSET_ZERO
                case 0x6: aluop = ALU_OPERATION.SLTU;braop = BRANCH_OPERATION.OFFSET_NZERO
                case 0x7: aluop = ALU_OPERATION.SLTU;braop = BRANCH_OPERATION.OFFSET_ZERO
            
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG(int(instr[20:25])),
                imm = int(instr[8:12]) << 1 + int(instr[25:31]) << 5 + int(instr[7]) << 11 + int(instr[12]) << 12,
                dst = REG.zero,
                srcs = SOURCE_SET.RS1_RS2,
                alu_op = aluop,
                res_route = RESULT_ROUTE.ALU_RD,
                bra_op = braop
            ) 
        case 0b1101111: # j-type JAL
            return instruction(
                rs1 = REG.zero,
                rs2 = REG.zero,
                imm = int(instr[21:31]) << 1 + int(instr[20]) << 11 + int(instr[12:19]) << 12 + int(instr[31]) << 20,
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_RS2,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.PC_RD_ALU_PC,
                bra_op = BRANCH_OPERATION.OFFSET_ALWAYS
            ) 
        case 0b1100111: # i-type JALR
            return instruction(
                rs1 = REG(int(instr[15:20])),
                rs2 = REG.zero,
                imm = int(instr[20:32]),
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_IMM,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.PC_RD_ALU_PC,
                bra_op = BRANCH_OPERATION.ABSOLUTE_ALU
            )
        case 0b0110111: # u-type LUI
            return instruction(
                rs1 = REG.zero,
                rs2 = REG.zero,
                imm = int(instr[20:32]) << 12,
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.RS1_IMM,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.ALU_RD,
                bra_op = BRANCH_OPERATION.NOBRANCH
            )
        case 0b0010111: # u-type auipc
            return instruction(
                rs1 = REG.zero,
                rs2 = REG.zero,
                imm = int(instr[20:32]) << 12,
                dst = REG(int(instr[7:12])),
                srcs = SOURCE_SET.PC_IMM,
                alu_op = ALU_OPERATION.ADD,
                res_route = RESULT_ROUTE.ALU_RD,
                bra_op = BRANCH_OPERATION.NOBRANCH
            )
        case _: return instruction() # unsupported -> NOP
    

        
def test_decoder_runner():  
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    
    rtl_sources = list((Path(__file__).parent.parent / "rtl").glob("*.sv"))
    testbench_source = Path(__file__).parent / "test_decoder.sv"
    sources = rtl_sources + [ testbench_source ]
    
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="test_decoder",
        build_dir=build_dir,
        always=True,
        waves=True
    )
    runner.test(
        hdl_toplevel="test_decoder", 
        test_module="test_decoder",
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    test_decoder_runner()