import logging
from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ReadWrite
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *
from bitint import *
    
@cocotb.test()
async def test_srcset_opts(dut):
    samples : list[dict[str, object]] = []
    
    await set_comb(dut, {
        "Imm" : word_t(0x696d6d).to_logicarray(),
        "PC"        : word_t(0x7063).to_logicarray(),
        "RS1"   : word_t(0x727331).to_logicarray(),
        "RS2"   : word_t(0x727332).to_logicarray()
    })
    
    await set_comb(dut, {
        "Set" :  source_set_e(SOURCE_SET.RS1_RS2).to_logicarray()
    })
    await sample_comb(dut, samples, [("A", "uint"), ("B", "uint")])
    
    await set_comb(dut, {
        "Set" : source_set_e(SOURCE_SET.RS1_IMM).to_logicarray()
    })
    await sample_comb(dut, samples, [("A", "uint"), ("B", "uint")])
    
    await set_comb(dut, {
        "Set" : source_set_e(SOURCE_SET.PC_IMM).to_logicarray()
    })
    await sample_comb(dut, samples, [("A", "uint"), ("B", "uint")])
    
    await set_comb(dut, {
        "Set" : source_set_e(SOURCE_SET.INVALID_0).to_logicarray()
    })
    await sample_comb(dut, samples, [("A", "uint"), ("B", "uint")])
    
    assert samples == [
        {"A":0x727331, "B":0x727332},
        {"A":0x727331, "B":0x696d6d},
        {"A":0x7063,   "B":0x696d6d},
        {"A":0,        "B":0}
    ]    
    
def test_source_mux_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_source_mux"
    
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
    test_source_mux_runner()