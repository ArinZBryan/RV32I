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
    dut.Do_Branch.value = Logic('0')
    dut.PC_branch_to.value = LogicArray.from_signed(0, TYPE_WORD_T)
    Clock(dut.Clk, 1, "us").start()
    await FallingEdge(dut.Clk)
    dut.Reset.value = Logic('1')
    
@cocotb.test()
async def advance_instruction_width(dut):
    """Test normal PC functionality"""
    
    await init_testbench(dut)
    
    pc_vals = []
    for i in range(0, 10):
        await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])
    
    assert(list(map(lambda x: x["PC"], pc_vals)) == [4, 8, 12, 16, 20, 24, 28, 32, 36, 40])
    
@cocotb.test()
async def jump(dut):
    """Test branching to specific addresses"""
    await init_testbench(dut)
    
    pc_vals = []
    
    # expected: []
    for i in range(0, 5):
        await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])
    
    await set_sync(dut, dut.Clk, {
        "PC_branch_to" : LogicArray.from_signed(4000, TYPE_WORD_T),
        "Do_Branch" : Logic('1')
    })
    
    await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])
    
    await set_sync(dut, dut.Clk, {
        "Do_Branch": Logic('0')
    })
    
    for i in range(0, 2):
        await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])
    
    await set_sync(dut, dut.Clk, {
        "PC_branch_to" : LogicArray.from_signed(1000, TYPE_WORD_T),
        "Do_Branch" : Logic('1')
    })
    
    await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])
    
    await set_sync(dut, dut.Clk, {
        "Do_Branch": Logic('0')
    })
    
    for i in range(0, 2):
        await sample_sync(dut, dut.Clk, pc_vals, [("PC", "int")])

    assert(list(map(lambda x: x["PC"], pc_vals)) == [4, 8, 12, 16, 20, 4000, 4004, 4008, 1000, 1004, 1008])
    
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