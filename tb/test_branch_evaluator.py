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
async def test_branch_evaluator(dut):
    samples = []
    
    # Initialisation
    await set_comb(dut, {
        "Var":word_t(1).to_logicarray(),
        "PC_Cur":word_t(0).to_logicarray(),
        "Offset":word_t(2).to_logicarray(),
        "Type":branch_op_e(BRANCH_OPERATION.NOBRANCH).to_logicarray()
    })
    
    # Forward Branching Tests
    await set_comb(dut, {"Type":branch_op_e(BRANCH_OPERATION.NOBRANCH).to_logicarray()})
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    await set_comb(dut, {
        "Type":branch_op_e(BRANCH_OPERATION.OFFSET_ZERO).to_logicarray(),
        "Var":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    await set_comb(dut, {
        "Type":branch_op_e(BRANCH_OPERATION.OFFSET_ZERO).to_logicarray(),
        "Var":word_t(1).to_logicarray()
    })
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    await set_comb(dut, {
        "Type":branch_op_e(BRANCH_OPERATION.OFFSET_NZERO).to_logicarray(),
        "Var":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    await set_comb(dut, {
        "Type":branch_op_e(BRANCH_OPERATION.OFFSET_NZERO).to_logicarray(),
        "Var":word_t(1).to_logicarray()
    })
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    await set_comb(dut, {
        "Type":branch_op_e(BRANCH_OPERATION.ALU).to_logicarray(),
        "Var":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("PC_Result", "uint")])
    
    assert samples == [
        {"PC_Result":4},         # nobranch - next insn
        {"PC_Result":2},         # zero (0) - immediate
        {"PC_Result":4},         # zero (1) - next insn
        {"PC_Result":4},         # nzero (1) - next insn
        {"PC_Result":2},         # nzero (0) - immediate
        {"PC_Result":0},         # ALU - immediate
    ]

def test_branch_evaluator_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_branch_evaluator"
    
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
    test_branch_evaluator_runner()