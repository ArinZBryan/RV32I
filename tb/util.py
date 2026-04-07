from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, ReadWrite, Timer
from aenum import IntEnum, NoAlias
from typing import Literal

TYPE_WORD_T = Range(31, 'downto', 0)
TYPE_REGREF_T = Range(4, 'downto', 0)
TYPE_ALURES_T = Range(32, 'downto', 0)

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

def REGtoLogicArray(reg : REG | int):
    return LogicArray.from_unsigned(reg, TYPE_REGREF_T)
def WORDtoLogicArray(word: int):
    return LogicArray.from_signed(word, TYPE_WORD_T)
def UWORDtoLogicArray(uword: int):
    return LogicArray.from_unsigned(uword, TYPE_WORD_T)
def ALUREStoLogicArray(alures: int):
    return LogicArray.from_signed(alures, TYPE_ALURES_T)

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