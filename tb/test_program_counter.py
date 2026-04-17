import logging
from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ReadWrite
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *


async def init_testbench(dut):
    """
    Sets up the clock, initialises `Do_Branch` and `PC_branch_to` to 0 and brings the testbench out of reset.
    """
    dut["_reset"].value = Logic('0')
    dut.PC_New.value = word_t(0).to_logicarray()
    Clock(dut.clock, 1, "us").start()
    await FallingEdge(dut.clock)
    dut["_reset"].value = Logic('1')
    
@cocotb.test()
async def test_program_counter(dut):
    await init_testbench(dut)
    
    samples = []
    
    await sample_sync(dut, dut.clock, samples, [("PC_Current", "uint"), ("PC_Next", "uint")])
    
    await set_sync(dut, dut.clock, {"PC_New": word_t(0x4000).to_logicarray()})
    await sample_sync(dut, dut.clock, samples, [("PC_Current", "uint"), ("PC_Next", "uint")])
    
    await set_sync(dut, dut.clock, {"PC_New": word_t(0x8000).to_logicarray()})
    await sample_sync(dut, dut.clock, samples, [("PC_Current", "uint"), ("PC_Next", "uint")])
    
    await set_sync(dut, dut.clock, {"PC_New": word_t(0x5000).to_logicarray()})
    await sample_sync(dut, dut.clock, samples, [("PC_Current", "uint"), ("PC_Next", "uint")])
    
    assert samples == [
        {"PC_Current":0,      "PC_Next":4}, 
        {"PC_Current":0x4000, "PC_Next":0x4004}, 
        {"PC_Current":0x8000, "PC_Next":0x8004}, 
        {"PC_Current":0x5000, "PC_Next":0x5004}
    ]
    
def test_program_counter_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    
    rtl_sources = list((Path(__file__).parent.parent / "rtl").glob("*.sv"))
    testbench_source = Path(__file__).parent / "test_program_counter.sv"
    sources = rtl_sources + [ testbench_source ]
    
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="test_program_counter",
        build_dir=build_dir,
        always=True,
        waves=True
    )
    runner.test(
        hdl_toplevel="test_program_counter", 
        test_module="test_program_counter",
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    test_program_counter_runner()