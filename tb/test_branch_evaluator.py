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
        "alu_result":word_t(1).to_logicarray(),
        "pc":word_t(0).to_logicarray(),
        "instr_imm":word_t(2).to_logicarray(),
        "branch_type":branch_op_e(BRANCH_OPERATION.INVALID_7).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    # Forward Branching Tests
    await set_comb(dut, {"branch_type":branch_op_e(BRANCH_OPERATION.NOBRANCH).to_logicarray()})
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_ZERO).to_logicarray(),
        "alu_result":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_ZERO).to_logicarray(),
        "alu_result":word_t(1).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_NZERO).to_logicarray(),
        "alu_result":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_NZERO).to_logicarray(),
        "alu_result":word_t(1).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_ALWAYS).to_logicarray(),
        "alu_result":word_t(0).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.ABSOLUTE_ALU).to_logicarray(),
        "alu_result":word_t(12).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])

    # Reverse branching test
    await set_comb(dut, {
        "branch_type":branch_op_e(BRANCH_OPERATION.OFFSET_ALWAYS).to_logicarray(),
        "pc":word_t(0x8000).to_logicarray(),
        "instr_imm":word_t(-12).to_logicarray()
    })
    await sample_comb(dut, samples, [("new_pc_value", "uint")])
    
    assert samples == [
        {"new_pc_value":0},         # invalid - no change
        {"new_pc_value":4},         # nobranch - next insn
        {"new_pc_value":2},         # zero (0) - immediate
        {"new_pc_value":4},         # zero (1) - next insn
        {"new_pc_value":4},         # nzero (1) - next insn
        {"new_pc_value":2},         # nzero (0) - immediate
        {"new_pc_value":2},         # always - immediate
        {"new_pc_value":12},        # absolute - alu value
        {"new_pc_value":0x8000-12}  # backwards always relative - -12
    ]

def test_source_mux_runner():
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
    test_source_mux_runner()