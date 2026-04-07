import logging
from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ReadWrite
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *
    
@cocotb.test()
async def test_srcset_opts(dut):
    samples : list[dict[str, object]] = []
    
    await set_comb(dut, {
        "input_instr_imm" : WORDtoLogicArray(0x696d6d),
        "input_pc"        : WORDtoLogicArray(0x7063),
        "input_reg_rs1"   : WORDtoLogicArray(0x727331),
        "input_reg_rs2"   : WORDtoLogicArray(0x727332)
    })
    
    await set_comb(dut, {
        "input_srcset" :  SRCSETtoLogicArray(SOURCE_SET.RS1_RS2)
    })
    await sample_comb(dut, samples, [("output_a", "uint"), ("output_b", "uint")])
    
    await set_comb(dut, {
        "input_srcset" : SRCSETtoLogicArray(SOURCE_SET.RS1_IMM)
    })
    await sample_comb(dut, samples, [("output_a", "uint"), ("output_b", "uint")])
    
    await set_comb(dut, {
        "input_srcset" : SRCSETtoLogicArray(SOURCE_SET.PC_IMM)
    })
    await sample_comb(dut, samples, [("output_a", "uint"), ("output_b", "uint")])
    
    await set_comb(dut, {
        "input_srcset" : SRCSETtoLogicArray(SOURCE_SET.INVALID_0)
    })
    await sample_comb(dut, samples, [("output_a", "uint"), ("output_b", "uint")])
    
    assert samples == [
        {"output_a":0x727331, "output_b":0x727332},
        {"output_a":0x727331, "output_b":0x696d6d},
        {"output_a":0x7063,   "output_b":0x696d6d},
        {"output_a":0,        "output_b":0}
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