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
async def test_ALU_RD(dut):
    samples : list[dict[str, object]] = []

    await set_comb(dut, {
        "Res_ALU"   : word_t(0x414c55).to_logicarray(),
        "PC_Next"   : word_t(0x5043).to_logicarray(),
        "RS2"       : word_t(0x525332).to_logicarray(),
        "Mem_RData" : word_t(0x4d454d59).to_logicarray()
    })
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_3).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[0] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x414c55,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_6).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[1] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x414c55,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.NONE).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[2] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x414c55,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[3] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x414c55,
        "Writeback_Enable" : Logic('1')
    }
        
@cocotb.test()
async def test_ALU_MEMREAD_RD(dut):
    samples : list[dict[str, object]] = []

    await set_comb(dut, {
        "Res_ALU"   : uword_t(0x414c55).to_logicarray(),
        "PC_Next"   : uword_t(0x5043).to_logicarray(),
        "RS2"       : uword_t(0x525332).to_logicarray(),
        "Mem_RData" : word_t(-1).to_logicarray()
    })
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_3).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[0] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_6).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[1] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.NONE).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[2] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S8).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[3] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : -1,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S8).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[4] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : -1,
        "Writeback_Enable" : Logic('1')
    }

    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[5] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : -1,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S32).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[6] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : -1,
        "Writeback_Enable" : Logic('1')
    }
  
    await set_comb(dut, {"Mem_RData" : uword_t(0x4d454d59).to_logicarray()})
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S32).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[7] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0x4d454d59,
        "Writeback_Enable" : Logic('1')
    }
  
    await set_comb(dut, {
        "Mem_RData" : uword_t(0x4d454d59).to_logicarray(),
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.U8).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[8] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0x00000059,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Mem_RData" : uword_t(0x4d454d59).to_logicarray(),
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMREAD_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.U16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[9] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0,
        "Writeback" : 0x00004d59,
        "Writeback_Enable" : Logic('1')
    }

@cocotb.test()
async def test_ALU_MEMWRITE(dut):
    samples : list[dict[str, object]] = []

    await set_comb(dut, {
        "Res_ALU"   : uword_t(0x414c55).to_logicarray(),
        "PC_Next"   : uword_t(0x5043).to_logicarray(),
        "RS2"       : uword_t(0x525332).to_logicarray(),
        "Mem_RData" : word_t(0x4d454d59).to_logicarray()
    })
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_3).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[0] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_6).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[1] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.NONE).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[2] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S8).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[3] == {
        "Mem_ByteSelect" : 0b0001,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }

    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[4] == {
        "Mem_ByteSelect" : 0b0011,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S32).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "int"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[5] == {
        "Mem_ByteSelect" : 0b1111,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
  
    await set_comb(dut, {
        "Mem_RData" : uword_t(0x4d454d59).to_logicarray(),
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.U8).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[6] == {
        "Mem_ByteSelect" : 0b0001,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }
    
    await set_comb(dut, {
        "Mem_RData" : uword_t(0x4d454d59).to_logicarray(),
        "Route" : result_route_e(RESULT_ROUTE.ALU_MEMWRITE).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.U16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[7] == {
        "Mem_ByteSelect" : 0b0011,
        "Mem_Addr" : 0x414c55,
        "Mem_WData" : 0x525332,
        "Writeback" : 0,
        "Writeback_Enable" : Logic('0')
    }

@cocotb.test()
async def test_PC_RD(dut):
    samples : list[dict[str, object]] = []

    await set_comb(dut, {
        "Res_ALU"   : word_t(0x414c55).to_logicarray(),
        "PC_Next"   : word_t(0x5043).to_logicarray(),
        "RS2"       : word_t(0x525332).to_logicarray(),
        "Mem_RData" : word_t(0x4d454d59).to_logicarray()
    })
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.PC_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_3).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[0] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x5043,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.PC_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.INVALID_6).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[1] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x5043,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.PC_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.NONE).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[2] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x5043,
        "Writeback_Enable" : Logic('1')
    }
    
    await set_comb(dut, {
        "Route" : result_route_e(RESULT_ROUTE.PC_RD).to_logicarray(),
        "Mem_Access_Size" : mem_access_size_e(MEMORY_SIZE.S16).to_logicarray(),
    })
    await sample_comb(dut, samples, [
        ("Mem_ByteSelect", "uint"),
        ("Mem_Addr", "uint"),
        ("Mem_WData", "uint"),
        ("Writeback", "uint"),
        ("Writeback_Enable", "unknown")
    ])
    assert samples[3] == {
        "Mem_ByteSelect" : 0,
        "Mem_Addr" : 0,
        "Mem_WData" : 0,
        "Writeback" : 0x5043,
        "Writeback_Enable" : Logic('1')
    }
       
        
def test_result_mux_runner():
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    test_bench = "test_result_mux"
    
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
    test_result_mux_runner()