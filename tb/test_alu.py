from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic
from cocotb.triggers import FallingEdge
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner


from util import *
from alu import *

@cocotb.test()
async def test_alu_instructions(dut):
    tests : list[tuple[alu_op_e, word_t, word_t]] = [
        (alu_op_e(ALU_OPERATION.ADD), word_t(0), word_t(0)),
        (alu_op_e(ALU_OPERATION.ADD), word_t(3), word_t(5)),
        (alu_op_e(ALU_OPERATION.SUB), word_t(5), word_t(3)),
        (alu_op_e(ALU_OPERATION.LSHL), word_t(3), word_t(3)),
        (alu_op_e(ALU_OPERATION.LSHL), word_t(-1), word_t(2)),
        (alu_op_e(ALU_OPERATION.LSHR), word_t(12), word_t(2)),
        (alu_op_e(ALU_OPERATION.LSHR), word_t(12), word_t(4)),
        (alu_op_e(ALU_OPERATION.LSHR), word_t(-1), word_t(2)),
        (alu_op_e(ALU_OPERATION.ASHR), word_t(12), word_t(2)),
        (alu_op_e(ALU_OPERATION.ASHR), word_t(12), word_t(4)),
        (alu_op_e(ALU_OPERATION.ASHR), word_t(-1), word_t(2)),
        (alu_op_e(ALU_OPERATION.SLT), word_t(1), word_t(2)),
        (alu_op_e(ALU_OPERATION.SLT), word_t(2), word_t(1)),
        (alu_op_e(ALU_OPERATION.SLT), word_t(-1), word_t(-2)),
        (alu_op_e(ALU_OPERATION.SLT), word_t(-2), word_t(-1)),
        (alu_op_e(ALU_OPERATION.SLTU), word_t(1), word_t(2)),
        (alu_op_e(ALU_OPERATION.SLTU), word_t(2), word_t(1)),
        (alu_op_e(ALU_OPERATION.OR), word_t(0b1010), word_t(0b1100)),
        (alu_op_e(ALU_OPERATION.XOR), word_t(0b1010), word_t(0b1100)),
        (alu_op_e(ALU_OPERATION.AND), word_t(0b1010), word_t(0b1100))
    ]
    
    for test in tests:
        sample = []
        cocotb.log.info(f"Test: {test[1].to_signed()} {ALU_OPERATION(test[0].to_unsigned()).__repr__()} {test[2].to_signed()}")
        await set_comb(dut, {
            "Op":test[0].to_logicarray(),
            "In_A":test[1].to_logicarray(),
            "In_B":test[2].to_logicarray()
        })
        await sample_comb(dut, sample, [("Out", "int")])
        assert py_alu_eval(*test).to_signed() == sample[0]["Out"]
    



def test_alu_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_alu"
    
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
    test_alu_runner()