from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, ReadWrite, Timer

from typing import Literal

TYPE_WORD_T = Range(31, 'downto', 0)

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