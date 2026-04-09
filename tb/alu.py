from cocotb.types import LogicArray, Range

from util import *

def py_alu_eval(alu_op : alu_op_e, a : word_t, b : word_t) -> word_t:
    if (a.size != 32 or b.size != 32):
        raise ValueError("argument sizes are not 32-bits")
    
    res = alures_t(0)
    
    match alu_op:
        case ALU_OPERATION.ADD: 
            res = a.signextend(33) + b.signextend(33)
        case ALU_OPERATION.SUB:
            res = a.signextend(33) - b.signextend(33)
        case ALU_OPERATION.LSHL:
            res = a.zeroextend(33).lshl(b.zeroextend(33) & 0b11111)
        case ALU_OPERATION.SLT:
            res = Bitint(1 if (a.signextend(33) < b.signextend(33)) else 0, 33, False)
        case ALU_OPERATION.SLTU:
            res = Bitint(1 if (a.zeroextend(33) < b.zeroextend(33)) else 0, 33, False)
        case ALU_OPERATION.XOR:
            res = a.zeroextend(33) ^ b.zeroextend(33)
        case ALU_OPERATION.LSHR:
            res = a.zeroextend(33).lshr(b.zeroextend(33) & 0b11111)
        case ALU_OPERATION.ASHR:
            res = a.signextend(33).ashr(b.zeroextend(33) & 0b11111)
        case ALU_OPERATION.OR:
            res = a.zeroextend(33) | b.zeroextend(33)
        case ALU_OPERATION.AND:
            res = a.zeroextend(33) & b.zeroextend(33)
    
    assert(res.size == 33)
    
    ret = word_t(0)
    ret.bits = res.bits & ret.numbitmask
    return ret