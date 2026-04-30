import logging
import sys
import os
import argparse
from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ReadWrite
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *

MEMORY_SIZE_BITS = 15

@cocotb.test()
async def run(dut):
    dut["_reset"].value = Logic('0')
    Clock(dut.clock, 1, "ns").start()
    await FallingEdge(dut.clock)
    
    program = Path(os.environ["COCOTB_PROGRAM"])
    timeout = int(os.environ["COCOTB_TIMEOUT"])
    signed = True if os.environ["COCOTB_SIGNED_RESULT"] == "True" else False
    memdump = Path(os.environ["COCOTB_MEMDUMP"])
    
    mem_contents = readmemb(str(program))
    for i in range(0, min(1 << MEMORY_SIZE_BITS, len(mem_contents))):
        dut.rv32i.module_memory.memory[i].value = mem_contents[i]   
    
    await FallingEdge(dut.clock)
    
    dut["_reset"].value = Logic('1')
    
    for i in range(timeout):
        await RisingEdge(dut.clock)
        if int(dut.rv32i.module_register_file.regs[31].value) == 1:
            break
    else:
        raise Exception(f"Program timed out after {timeout} cycles")

    return_value : LogicArray = dut.rv32i.module_register_file.regs[10].value  
    
    assert (int(return_value) == 42)
    


def test_program_runner():
    parser = argparse.ArgumentParser()
    
    args = parser.parse_args()
    os.environ["COCOTB_PROGRAM"] = str(Path(__file__).parent.parent / "c" / "test" / "program.bin")
    os.environ["COCOTB_TIMEOUT"] = str(10_000)
    os.environ["COCOTB_SIGNED_RESULT"] = str(False)
    os.environ["COCOTB_MEMDUMP"] = ""
    
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    top_file = "top_RV32I"
    
    rtl_sources = list((Path(__file__).parent.parent / "rtl").glob("*.sv"))
    testbench_source = Path(__file__).parent / f"{top_file}.sv"
    sources = rtl_sources + [ testbench_source ]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=top_file,
        build_dir=build_dir,
        always=True,
        waves=True
    )
    runner.test(
        hdl_toplevel=top_file, 
        test_module="test_instructions",
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    test_program_runner()