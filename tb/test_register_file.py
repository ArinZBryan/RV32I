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
    Sets up the clock, initialises control signals to 0, unsets write_enable and brings the testbench out of reset.
    """
    dut["_reset"].value = Logic('0')
    dut["Select_rs1"].value = regref_t(REG.zero).to_logicarray()
    dut["Select_rs2"].value = regref_t(REG.zero).to_logicarray()
    dut["WSelect"].value = regref_t(REG.zero).to_logicarray()
    dut["WData"].value = word_t(12).to_logicarray()
    dut["WE"].value = Logic('0')
    
    Clock(dut.clock, 1, "us").start()
    await FallingEdge(dut.clock)
    dut["_reset"].value = Logic('1')
    
@cocotb.test()
async def test_read_x0(dut):
    await init_testbench(dut)
    
    samples : list[dict[str, object]] = []
    
    await set_sync(dut, dut.clock, {
        "Select_rs1" : regref_t(REG.zero).to_logicarray(),
        "Select_rs2" : regref_t(REG.zero).to_logicarray()
    })
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    assert samples == [{"Out_rs1":0,"Out_rs2":0}]    

@cocotb.test()
async def test_write_read_x0(dut):
    await init_testbench(dut)
    
    samples : list[dict[str, object]] = []
    
    await set_sync(dut, dut.clock, {
        "Select_rs1" : regref_t(REG.zero).to_logicarray(),
        "Select_rs2" : regref_t(REG.zero).to_logicarray(),
        "WE" : Logic('1'),
        "WData": word_t(1).to_logicarray(),
        "WSelect": regref_t(REG.zero).to_logicarray()
    })
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    assert samples == [{"Out_rs1":0,"Out_rs2":0}]  

@cocotb.test()
async def test_write_read_x1x2(dut):
    await init_testbench(dut)
    
    samples : list[dict[str, object]] = []
    
    await set_sync(dut, dut.clock, {
        "Select_rs1" : regref_t(1).to_logicarray(),
        "Select_rs2" : regref_t(2).to_logicarray(),
        "WE" : Logic('1'),
        "WData": word_t(1).to_logicarray(),
        "WSelect": regref_t(1).to_logicarray()
    })
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    await set_sync(dut, dut.clock, {
        "WData": word_t(2).to_logicarray(),
        "WSelect": regref_t(2).to_logicarray()
    })
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    assert samples == [{"Out_rs1":1,"Out_rs2":0}, {"Out_rs1":1,"Out_rs2":2}]  

@cocotb.test()
async def test_write_enable(dut):
    await init_testbench(dut)
    
    samples : list[dict[str, object]] = []
    
    await set_sync(dut, dut.clock, {
        "Select_rs1" : regref_t(1).to_logicarray(),
        "Select_rs2" : regref_t(REG.zero).to_logicarray(),
        "WE" : Logic('0'),
        "WData": word_t(1).to_logicarray(),
        "WSelect": regref_t(1).to_logicarray()
    })
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    await set_sync(dut, dut.clock, {"WE": Logic('1')})
    await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint"), ("Out_rs2", "uint")])
    assert samples == [{"Out_rs1":0,"Out_rs2":0}, {"Out_rs1":1,"Out_rs2":0}]  

@cocotb.test()
async def test_write_read_allregs(dut):
    await init_testbench(dut)
    
    samples : list[dict[str, object]] = []
    
    for i in range(0, 32):
        await set_sync(dut, dut.clock, {
            "WE" : Logic('1'),
            "WData": word_t(i).to_logicarray(),
            "WSelect": regref_t(i).to_logicarray()
        })
    for i in range(0, 32):
        await set_sync(dut, dut.clock, {
            "WE" : Logic('0'),
            "Select_rs1": regref_t(i).to_logicarray(),
        })
        await sample_sync(dut, dut.clock, samples, [("Out_rs1", "uint")])
    
    assert samples == [{"Out_rs1":i} for i in range(0, 32)]  

def test_register_file_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_register_file"
    
    rtl_sources = list((Path(__file__).parent.parent / "rtl").glob("*.sv"))
    testbench_source = Path(__file__).parent / f"{test_bench}.sv"
    sources = rtl_sources + [ testbench_source ]
    
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=test_bench,
        build_dir=build_dir,
        always=True,
        waves=True
    )
    runner.test(
        hdl_toplevel=test_bench, 
        test_module=test_bench,
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    test_register_file_runner()