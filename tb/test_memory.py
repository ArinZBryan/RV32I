import logging
from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic, Range
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ReadOnly, ReadWrite
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner

from util import *

MEM_SIZE_BITS = 16

async def init_testbench(dut):
    """
    Sets up the clock, initialises control signals to 0, unsets write_enable and brings the testbench out of reset.
    """
    dut["PortA_Addr"].value = uword_t(0).to_logicarray()
    dut["PortA_WData"].value = uword_t(0).to_logicarray()
    dut["PortA_WriteSelect"].value = byte_select_t(0).to_logicarray()
    dut["PortB_Addr"].value = uword_t(0).to_logicarray()
    dut["PortB_WData"].value = uword_t(0).to_logicarray()
    dut["PortB_WriteSelect"].value = byte_select_t(0).to_logicarray()
    
    mem_contents = readmemb(str(Path(__file__).parent / "65536_random_bytes.bin"))
    for i in range(0, 1 << 16):
        dut.mem.memory[i].value = mem_contents[i]   
    
    Clock(dut.clock, 1, "us").start()
    await FallingEdge(dut.clock)
    
    #return [LogicArray(0, Range(7, 'downto', 0)) for i in range(65536)] 
    return mem_contents
    
    
async def sv_mem_read(dut, clk, addr_a : uword_t | int, addr_b : uword_t | int):
    sample = []
    await set_sync(dut, clk, {
        "PortA_Addr" : coerce_to_u32_bits(addr_a).to_logicarray(),
        "PortB_Addr" : coerce_to_u32_bits(addr_b).to_logicarray(),
        "PortA_WriteSelect" : byte_select_t(0).to_logicarray(),
        "PortB_WriteSelect" : byte_select_t(0).to_logicarray()
    })
    await sample_sync(dut, clk, sample, [("PortA_Out", "uint"), ("PortB_Out", "uint")])
    return sample[0]
    
async def sv_mem_write(dut, clk, addr_a : uword_t | int, addr_b : uword_t | int, val_a : word_t | uword_t | int, val_b : word_t | uword_t | int, bytes_a : byte_select_t | int, bytes_b : byte_select_t | int):
    await set_sync(dut, clk, {
        "PortA_Addr" : coerce_to_u32_bits(addr_a).to_logicarray(),
        "PortB_Addr" : coerce_to_u32_bits(addr_b).to_logicarray(),
        "PortA_WData" : coerce_to_u32_bits(val_a).to_logicarray(),
        "PortB_WData" : coerce_to_u32_bits(val_b).to_logicarray(),
        "PortA_WriteSelect" : (byte_select_t(bytes_a) if isinstance(bytes_a, int) else bytes_a).to_logicarray(),
        "PortB_WriteSelect" : (byte_select_t(bytes_b) if isinstance(bytes_b, int) else bytes_b).to_logicarray()
    })
    
def py_mem_read(mem : list[LogicArray], addr_a : uword_t | int, addr_b : uword_t | int):
    addr_a_int = (addr_a.to_unsigned() if isinstance(addr_a, uword_t) else addr_a) & ((1 << MEM_SIZE_BITS) - 1)
    addr_b_int = (addr_b.to_unsigned() if isinstance(addr_b, uword_t) else addr_b) & ((1 << MEM_SIZE_BITS) - 1)
    
    return {
        "PortA_Out": (
            uword_t(mem[addr_a_int + 3].to_unsigned()) << 24 |
            uword_t(mem[addr_a_int + 2].to_unsigned()) << 16 |
            uword_t(mem[addr_a_int + 1].to_unsigned()) << 8  |
            uword_t(mem[addr_a_int    ].to_unsigned())
        ).to_unsigned(),
        "PortB_Out": (
            uword_t(mem[addr_b_int + 3].to_unsigned()) << 24 |
            uword_t(mem[addr_b_int + 2].to_unsigned()) << 16 |
            uword_t(mem[addr_b_int + 1].to_unsigned()) << 8  |
            uword_t(mem[addr_b_int    ].to_unsigned())
        ).to_unsigned()
    }

def py_mem_write(mem : list[LogicArray], addr_a : uword_t | int, addr_b : uword_t | int, val_a : uword_t | word_t | int, val_b : uword_t | word_t | int, bytes_a : byte_select_t | int, bytes_b : byte_select_t | int):
    addr_a_int = coerce_to_u32_bits(addr_a).to_unsigned() & ((1 << MEM_SIZE_BITS) - 1)
    addr_b_int = coerce_to_u32_bits(addr_b).to_unsigned() & ((1 << MEM_SIZE_BITS) - 1)
    val_a_word = coerce_to_u32_bits(val_a)
    val_b_word = coerce_to_u32_bits(val_b)
    
    if (bytes_a & 0b0001) == 1:
        mem[addr_a_int]     = ((val_a_word & 0x000000ff) >> 0).to_logicarray()
    if (bytes_a & 0b0010) >> 1 == 1:
        mem[addr_a_int + 1] = ((val_a_word & 0x0000ff00) >> 8).to_logicarray()
    if (bytes_a & 0b0100) >> 2 == 1:
        mem[addr_a_int + 2] = ((val_a_word & 0x00ff0000) >> 16).to_logicarray()
    if (bytes_a & 0b1000) >> 3 == 1:
        mem[addr_a_int + 3] = ((val_a_word & 0xff000000) >> 24).to_logicarray()
        
    if (bytes_b & 0b0001) == 1:
        mem[addr_b_int]     = ((val_b_word & 0x000000ff) >> 0).to_logicarray()
    if (bytes_b & 0b0010) >> 1 == 1:
        mem[addr_b_int + 1] = ((val_b_word & 0x0000ff00) >> 8).to_logicarray()
    if (bytes_b & 0b0100) >> 2 == 1:
        mem[addr_b_int + 2] = ((val_b_word & 0x00ff0000) >> 16).to_logicarray()
    if (bytes_b & 0b1000) >> 3 == 1:
        mem[addr_b_int + 3] = ((val_b_word & 0xff000000) >> 24).to_logicarray()
    
@cocotb.test()
async def test_read_once_ab(dut):
    pymem = await init_testbench(dut)
    
    assert py_mem_read(pymem, 12, 12) == await sv_mem_read(dut, dut.clock, 12, 12)
    assert py_mem_read(pymem, 8, 16) == await sv_mem_read(dut, dut.clock, 8, 16)
    
@cocotb.test()
async def test_read_write_selects(dut):
    pymem = await init_testbench(dut)
    
    for i in range (0, 0b10000):
        cocotb.log.info(f"write select: {i}")
        addr_a = i*4
        addr_b = addr_a + 64
        
        py_mem_write(pymem, addr_a, addr_b, -1, -1, i, i)
        await sv_mem_write(dut, dut.clock, addr_a, addr_b, -1, -1, i, i)
        assert py_mem_read(pymem, addr_a, addr_b) == await sv_mem_read(dut, dut.clock, addr_a, addr_b)
    
@cocotb.test()
async def test_write_to_same_addr(dut):
    pymem = await init_testbench(dut)
    
    py_mem_write(pymem, 12, 12, -1, 0, 0b1111, 0b1111)
    await sv_mem_write(dut, dut.clock, 12, 12, -1, 0, 0b1111, 0b1111)
    assert py_mem_read(pymem, 12, 12) == await sv_mem_read(dut, dut.clock, 12, 12)
    
@cocotb.test()
async def test_write_oob(dut):
    pymem = await init_testbench(dut)
    
    py_mem_write(pymem, 0x00200000, 0x00200004, -1, -1, 0b1111, 0b1111)
    await sv_mem_write(dut, dut.clock, 0x00200000, 0x00200004, -1, -1, 0b1111, 0b1111)
    assert py_mem_read(pymem, 0x00200000, 0x00200004) == await sv_mem_read(dut, dut.clock, 0x00200000, 0x00200004)
    assert await sv_mem_read(dut, dut.clock, 0x00200000, 0x00200004) == await sv_mem_read(dut, dut.clock, 0, 4)

#@cocotb.test()
#async def test_fail(dut):
#    raise AssertionError()
    
def test_register_file_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_memory"
    
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