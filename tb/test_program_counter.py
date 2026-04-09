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
    dut.Reset.value = Logic('0')
    dut.PC_branch_to.value = LogicArray.from_signed(0, TYPE_WORD_T)
    Clock(dut.Clk, 1, "us").start()
    await FallingEdge(dut.Clk)
    dut.Reset.value = Logic('1')
    
@cocotb.test()
async def test_program_counter(dut):
    await init_testbench(dut)
    
    samples = []
    
    await sample_sync(dut, dut.Clk, samples, [("PC", "uint")])
    
    await set_sync(dut, dut.Clk, {"PC_branch_to": word_t(0x4000).to_logicarray()})
    await sample_sync(dut, dut.Clk, samples, [("PC", "uint")])
    
    await set_sync(dut, dut.Clk, {"PC_branch_to": word_t(0x8000).to_logicarray()})
    await sample_sync(dut, dut.Clk, samples, [("PC", "uint")])
    
    await set_sync(dut, dut.Clk, {"PC_branch_to": word_t(0x5000).to_logicarray()})
    await sample_sync(dut, dut.Clk, samples, [("PC", "uint")])
    
    assert samples == [{"PC":0}, {"PC":0x4000}, {"PC":0x8000}, {"PC":0x5000}]
    
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