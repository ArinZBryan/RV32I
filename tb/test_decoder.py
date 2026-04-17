from pathlib import Path

import cocotb
from cocotb.types import LogicArray, Logic
from cocotb.triggers import FallingEdge
from cocotb.clock import Clock
from cocotb_tools.runner import get_runner


from util import *
from decoder import *

    
@cocotb.test()
async def decode_valid_r_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
    "add"  : raw_instruction.encode_r(0b0110011, REG(0),  0, REG(1),  REG(2),  0x00),
    "sub"  : raw_instruction.encode_r(0b0110011, REG(3),  0, REG(4),  REG(5),  0x20),
    "xor"  : raw_instruction.encode_r(0b0110011, REG(6),  4, REG(7),  REG(8),  0x00),
    "or_"  : raw_instruction.encode_r(0b0110011, REG(9),  6, REG(10), REG(11), 0x00),
    "and_" : raw_instruction.encode_r(0b0110011, REG(12), 7, REG(13), REG(14), 0x00),
    "sll"  : raw_instruction.encode_r(0b0110011, REG(15), 1, REG(16), REG(17), 0x00),
    "srl"  : raw_instruction.encode_r(0b0110011, REG(18), 5, REG(19), REG(20), 0x00),
    "sra"  : raw_instruction.encode_r(0b0110011, REG(21), 5, REG(22), REG(23), 0x20),
    "slr"  : raw_instruction.encode_r(0b0110011, REG(24), 2, REG(25), REG(26), 0x00),
    "sltu" : raw_instruction.encode_r(0b0110011, REG(27), 3, REG(28), REG(29), 0x00),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])
    
@cocotb.test()
async def decode_unsupported_instruction(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
    "fence"      : raw_instruction.encode_i(0b0001111, REG.zero,  0, REG.zero, 0),
    "fence_i"    : raw_instruction.encode_i(0b0001111, REG.zero,  1, REG.zero, 0),
    "csrrw"      : raw_instruction.encode_i(0b1110011, REG(1), 1, REG(2), 0),
    "csrrs"      : raw_instruction.encode_i(0b1110011, REG(1), 2, REG(2), 0),
    "csrrc"      : raw_instruction.encode_i(0b1110011, REG(1), 3, REG(2), 0),
    "csrrwi"     : raw_instruction.encode_i(0b1110011, REG(1), 5, REG(2), 0),
    "csrrsi"     : raw_instruction.encode_i(0b1110011, REG(1), 6, REG(2), 0),
    "csrrci"     : raw_instruction.encode_i(0b1110011, REG(1), 7, REG(2), 0),
    "ecall"      : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 0),
    "ebreak"     : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 1),
    "uret"       : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 2),
    "sret"       : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 0b000100000010),
    "mret"       : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 0b001100000010),
    "wfi"        : raw_instruction.encode_i(0b1110011, REG.zero, 1, REG.zero, 0b000100000101),
    "sfence_vma" : raw_instruction.encode_r(0b1110011, REG(1), 1, REG(2), REG(3),  0b0001001),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])
        
@cocotb.test()
async def decode_valid_i_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
        "addi"  : raw_instruction.encode_i(0b0010011, REG(1), 0, REG(2), 0),
        "xori"  : raw_instruction.encode_i(0b0010011, REG(3), 4, REG(4), 0),
        "ori"   : raw_instruction.encode_i(0b0010011, REG(5), 6, REG(6), 0),
        "andi"  : raw_instruction.encode_i(0b0010011, REG(7), 7, REG(8), 0),
        "slli"  : raw_instruction.encode_i(0b0010011, REG(9), 1, REG(10), 0),
        "srli"  : raw_instruction.encode_i(0b0010011, REG(11), 5, REG(12), 0),
        "srai"  : raw_instruction.encode_i(0b0010011, REG(13), 5, REG(14), 0b0000001_00000),
        "slti"  : raw_instruction.encode_i(0b0010011, REG(15), 2, REG(16), 0),
        "sltiu" : raw_instruction.encode_i(0b0010011, REG(17), 3, REG(18), 0),
        "lb"    : raw_instruction.encode_i(0b0100011, REG(19), 0, REG(20), 0),
        "lh"    : raw_instruction.encode_i(0b0010011, REG(21), 1, REG(22), 0),
        "lw"    : raw_instruction.encode_i(0b0010011, REG(23), 2, REG(24), 0),
        "lbu"   : raw_instruction.encode_i(0b0010011, REG(25), 4, REG(26), 0),
        "lhu"   : raw_instruction.encode_i(0b0010011, REG(27), 5, REG(28), 0),
        "jalr"  : raw_instruction.encode_i(0b1100111, REG(29), 0, REG(30), 0),  
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_invalid_i_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
        "l3"  : raw_instruction.encode_i(0b0000011, REG(1), 3, REG(2), 0),
        "l6"  : raw_instruction.encode_i(0b0000011, REG(3), 6, REG(4), 0),
        "l7"   : raw_instruction.encode_i(0b0000011, REG(5), 7, REG(6), 0),
        "jalr1"  : raw_instruction.encode_i(0b1100111, REG(29), 1, REG(30), 0),  
        "jalr2"  : raw_instruction.encode_i(0b1100111, REG(29), 2, REG(30), 0),  
        "jalr3"  : raw_instruction.encode_i(0b1100111, REG(29), 3, REG(30), 0),  
        "jalr4"  : raw_instruction.encode_i(0b1100111, REG(29), 4, REG(30), 0),  
        "jalr5"  : raw_instruction.encode_i(0b1100111, REG(29), 5, REG(30), 0),  
        "jalr6"  : raw_instruction.encode_i(0b1100111, REG(29), 6, REG(30), 0),  
        "jalr7"  : raw_instruction.encode_i(0b1100111, REG(29), 7, REG(30), 0)
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_valid_s_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
    "sb"  : raw_instruction.encode_s(0b0110011, 0, REG(1),  REG(2),  0),
    "sh"  : raw_instruction.encode_s(0b0110011, 1, REG(4),  REG(5),  0),
    "sw"  : raw_instruction.encode_s(0b0110011, 2, REG(7),  REG(8),  0),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_invalid_s_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
    "sinvalid_3"  : raw_instruction.encode_s(0b0110011, 3, REG(1),  REG(2),  0),
    "sinvalid_4"  : raw_instruction.encode_s(0b0110011, 4, REG(4),  REG(5),  0),
    "sinvalid_5"  : raw_instruction.encode_s(0b0110011, 5, REG(7),  REG(8),  0),
    "sinvalid_6"  : raw_instruction.encode_s(0b0110011, 6, REG(9),  REG(10),  0),
    "sinvalid_7"  : raw_instruction.encode_s(0b0110011, 7, REG(11),  REG(12),  0),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_valid_b_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
    "beq"  : raw_instruction.encode_b(0b1100011, CMP_TYPE.EQ,  REG(1), REG(2), 12),
    "bne"  : raw_instruction.encode_b(0b1100011, CMP_TYPE.NEQ, REG(1), REG(2), 12),
    "blt"  : raw_instruction.encode_b(0b1100011, CMP_TYPE.LT,  REG(1), REG(2), 12),
    "bge"  : raw_instruction.encode_b(0b1100011, CMP_TYPE.GE,  REG(1), REG(2), 12),
    "bltu" : raw_instruction.encode_b(0b1100011, CMP_TYPE.LTU, REG(1), REG(2), 12),
    "bgeu" : raw_instruction.encode_b(0b1100011, CMP_TYPE.GEU, REG(1), REG(2), 12),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info("python: " + instruction(py_decoded_instrs[i]).to_str())
        cocotb.log.info("rtl: " + instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])
  
@cocotb.test()
async def decode_invalid_b_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
        "binvalid_2" : raw_instruction.encode_b(0b1100011, CMP_TYPE.INVALID_2, REG(1), REG(2), 12),
        "binvalid_3" : raw_instruction.encode_b(0b1100011, CMP_TYPE.INVALID_3, REG(1), REG(2), 12),
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info(instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_valid_j_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
        "jal" : raw_instruction.encode_j(0b1101111, REG(0), 10000)
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info("python: " + instruction(py_decoded_instrs[i]).to_str())
        cocotb.log.info("rtl: " + instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

@cocotb.test()
async def decode_valid_u_instructions(dut):
    py_decoded_instrs : list[instruction] = []
    sv_decoded_instrs = []
    raw_instrs = {
        "lui" : raw_instruction.encode_u(0b0110111, REG(1), -1),
        "auipc" : raw_instruction.encode_u(0b0010111, REG(2), -1)
    }
    
    for _,v in raw_instrs.items():
        await set_comb(dut, {"Raw" : v })
        await sample_comb(dut, sv_decoded_instrs, [("Decoded", "unknown")])
        py_decoded_instrs.append(decode(v))
        
    for i in range(0, len(py_decoded_instrs)):
        cocotb.log.info("python: " + instruction(py_decoded_instrs[i]).to_str())
        cocotb.log.info("rtl: " + instruction(sv_decoded_instrs[i]["Decoded"]).to_str())
        assert str(py_decoded_instrs[i]) == str(sv_decoded_instrs[i]["Decoded"])

def test_decoder_runner():  
    sim = "verilator"
    build_dir = Path(__file__).parent.parent / "build"
    
    rtl_sources = list((Path(__file__).parent.parent / "rtl").glob("*.sv"))
    testbench_source = Path(__file__).parent / "test_decoder.sv"
    sources = rtl_sources + [ testbench_source ]
    
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="test_decoder",
        build_dir=build_dir,
        always=True,
        waves=True
    )
    runner.test(
        hdl_toplevel="test_decoder", 
        test_module="test_decoder",
        hdl_toplevel_lang="verilog",
        waves=True,
        verbose=True
    )
    
if __name__ == "__main__":
    test_decoder_runner()