from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, ReadWrite, Timer
from aenum import IntEnum, NoAlias
from typing import Literal
from bitint import Bitint

TYPE_WORD_T = Range(31, 'downto', 0)
TYPE_REGREF_T = Range(4, 'downto', 0)
TYPE_ALURES_T = Range(32, 'downto', 0)
TYPE_SOURCE_SET_E = Range(1, 'downto', 0)
TYPE_BRANCH_OP_E = Range(2, 'downto', 0)
TYPE_RESULT_ROUTE_E = Range(1, 'downto', 0)
TYPE_ALU_OP_E = Range(3, 'downto', 0)

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

# typdef enum logic[4:0] { ... } alu_op_t
class ALU_OPERATION(IntEnum):
    ADD =  0b0000 # d0   h0
    LSHL = 0b0001 # d1   h1
    SLT =  0b0010 # d2   h2
    SLTU = 0b0011 # d3   h3
    XOR =  0b0100 # d4   h4
    LSHR = 0b0101 # d5   h5
    OR  =  0b0110 # d6   h6
    AND =  0b0111 # d7   h7
    
    SUB =  0b1000 # d8   h8
    NOP9 = 0b1001 # d9   h9
    NOPA = 0b1010 # d10  hA
    NOPB = 0b1011 # d11  hB
    NOPC = 0b1100 # d12  hC
    ASHR = 0b1101 # d13  h13
    NOPE = 0b1110 # d14  h14
    NOPF = 0b1111 # d15  h15
    
# typdef enum logic[1:0] { ... } res_route_t
class RESULT_ROUTE(IntEnum):
    ALU_RD = 0
    ALU_MEMREAD_RD = 1
    ALU_MEMWRITE = 2
    PC_RD = 3

# typedef enum logic[1:0] { ... } bra_op_t
class BRANCH_OPERATION(IntEnum):
    NOBRANCH = 0
    OFFSET_ZERO = 1
    OFFSET_NZERO = 2
    ALU = 3

# typedef enum logic[1:0] { ... } src_set_t
class SOURCE_SET(IntEnum):
    RS1_RS2 = 0b10
    RS1_IMM = 0b11
    PC_IMM =  0b01
    INVALID_0 = 0b00
    
# typedef enum logic[2:0] { ... } mem_access_size_e
class MEMORY_SIZE(IntEnum):
    S8  = 0b000
    S16 = 0b001
    S32 = 0b010
    INVALID_3 = 0b011
    U8  = 0b100
    U16 = 0b101
    INVALID_6 = 0b110
    NONE = 0b111
        
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


async def sample_sync(dut, clock, sampleArray: list[dict[str, object]], values: list[tuple[str, Literal["int", "uint", "unknown"]]]):
    """Samples values when they will have settled after the next clock pulse."""
    
    await RisingEdge(clock)
    await ReadOnly()
    new_samples = {}
    for sample_point, sample_value in values:
        if (sample_value == "int"):
            new_samples[sample_point] = dut[sample_point].value.to_signed()
        elif (sample_value == "uint"):
            new_samples[sample_point] = dut[sample_point].value.to_unsigned()
        else:
            new_samples[sample_point] = dut[sample_point].value
    sampleArray.append(new_samples)

async def sample_comb(dut, sampleArray: list[dict[str, object]], values: list[tuple[str, Literal["int", "uint", "unknown"]]]):
    """Samples values when they will next be settled. Use only with purely-combinational DUTs"""
    await Timer(1, unit='ps')
    await ReadOnly()
    new_samples = {}
    for sample_point, sample_value in values:
        if (sample_value == "int"):
            new_samples[sample_point] = dut[sample_point].value.to_signed()
        elif (sample_value == "uint"):
            new_samples[sample_point] = dut[sample_point].value.to_unsigned()
        else:
            new_samples[sample_point] = dut[sample_point].value
    sampleArray.append(new_samples)

async def set_sync(dut, clock, values: dict[str, object]):
    """Sets values in the next period in the clock when it is safe to set values."""
    
    await FallingEdge(clock)
    await ReadWrite()
    for (k, v) in values.items():
        dut[k].value = v
        
async def set_comb(dut, values: dict[str, object]):
    """Sets values at the next available opportunity. Use only with purely-combinational DUTs"""
    
    await Timer(1, unit="ps")
    await ReadWrite()
    for (k, v) in values.items():
        dut[k].value = v
        
class word_t(Bitint):
    def __init__(self, pyint: int):
        super().__init__(pyint, 32, True)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 32, True)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(32, True)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(32, True)

class uword_t(Bitint):
    def __init__(self, pyint: int):
        super().__init__(pyint, 32, False)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 32, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(32, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(32, False)

class regref_t(Bitint):
    def __init__(self, pyint: int | REG):
        super().__init__(int(pyint), 5, False)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 5, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(5, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(5, False)
        
class alures_t(Bitint):
    def __init__(self, pyint: int):
        super().__init__(pyint, 33, True)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 33, True)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(33, True)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(33, True)
        
class alu_op_e(Bitint):
    def __init__(self, pyint: int | ALU_OPERATION):
        super().__init__(int(pyint), 4, False)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 4, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(4, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(4, False)

class source_set_e(Bitint):
    def __init__(self, pyint: int | SOURCE_SET):
        super().__init__(int(pyint), 2, False)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 2, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(2, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(2, False)
        
class result_route_e(Bitint):
    def __init__(self, pyint: int | RESULT_ROUTE):
        super().__init__(int(pyint), 2, False)
        
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 2, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(2, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(2, False)
        
class branch_op_e(Bitint):
    def __init__(self, pyint: int | BRANCH_OPERATION):
        super().__init__(int(pyint), 2, False)
        
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 2, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(3, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(3, False)
        
class mem_access_size_e(Bitint):
    def __init__(self, pyint: int | MEMORY_SIZE):
        super().__init__(int(pyint), 3, False)
        
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 3, False)
    
    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(3, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(3, False)

class byte_select_t(Bitint):
    def __init__(self, pyint: int):
        super().__init__(int(pyint), 4, False)
    
    @staticmethod
    def representable(pyint: int):
        return Bitint.representable(pyint, 4, False)

    @staticmethod
    def maxvalue() -> int:
        return Bitint.maxvalue(4, False)
    
    @staticmethod
    def minvalue() -> int:
        return Bitint.minvalue(4, False)
   
def coerce_to_u32_bits(v: int | uword_t | word_t) -> uword_t:
    if isinstance(v, int):
        if uword_t.representable(v):
            return uword_t(v)
        elif word_t.representable(v):
            return uword_t(word_t(v).to_unsigned())
        else:
            raise ArithmeticError(f"Cannot coerce value {v} to 32-bit signed/unsigned integer")
    elif isinstance(v, Bitint):
        return uword_t(v.to_unsigned())
    else:
        raise ValueError("val_a not of integer type")

def coerce_to_s32_bits(v: int | uword_t | word_t) -> word_t:
    if isinstance(v, int):
        if word_t.representable(v):
            return word_t(v)
        elif uword_t.representable(v):
            return word_t(uword_t(v).to_unsigned())
        else:
            raise ArithmeticError(f"Cannot coerce value {v} to 32-bit signed/unsigned integer")
    elif isinstance(v, Bitint):
        return word_t(v.to_signed())
    else:
        raise ValueError("val_a not of integer type")
   
def readmemb(path : str):
    file = open(path, "rb")
    file_bytes = file.read()
    res = [LogicArray(b, Range(7, 'downto', 0)) for b in file_bytes]
    file.close()
    return res