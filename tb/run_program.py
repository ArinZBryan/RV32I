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

MEMORY_SIZE_BITS = 10
PROGRAM_MAXIMUM_CYCLES = 100_000

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
        if memdump != "":
            size = 1 << MEMORY_SIZE_BITS
            data = bytearray(size)
            mem = dut.rv32i.module_memory.memory
            for i in range(size):
                if i % 100 == 0:
                    cocotb.log.info(i)
                data[i] = mem[i].value.to_unsigned() & 0xFF
            memdump.write_bytes(data)    
        raise Exception(f"Program timed out after {timeout} cycles")

    return_value : LogicArray = dut.rv32i.module_register_file.regs[10].value
    
    if memdump != "":
        size = 1 << MEMORY_SIZE_BITS
        data = bytearray(size)
        mem = dut.rv32i.module_memory.memory
        for i in range(size):
            if i % 100 == 0:
                cocotb.log.info(i)
            data[i] = mem[i].value.to_unsigned() & 0xFF
        memdump.write_bytes(data)    
    
    cocotb.log.critical(f"Exited with return value {int(return_value) if signed else return_value.to_unsigned()}")
    


def run_program():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--program",
        type=str,
        help=f"Path to the memory snapshot containing the program binary to run. Must not be larger than {1<<MEMORY_SIZE_BITS} bytes large."
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        help=f"Number of CPU cycles to execute before forcefully ending simulation."
    )
    parser.add_argument(
        "-s", "--signed",
        action=argparse.BooleanOptionalAction,
        help=f"Interpret the return value of the program (the value left in x10/a0 at the end of the simulation) as a signed integer instead of an unsigned integer."
    )
    parser.add_argument(
        "-m", "--memdump",
        type=str,
        help="Path to the memory snapshot produced after the program has run."
    )
    args = parser.parse_args()
    os.environ["COCOTB_PROGRAM"] = args.program
    os.environ["COCOTB_TIMEOUT"] = str(args.timeout)
    os.environ["COCOTB_SIGNED_RESULT"] = str(args.signed)
    os.environ["COCOTB_MEMDUMP"] = args.memdump
    
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
        test_module="run_program",
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    run_program()