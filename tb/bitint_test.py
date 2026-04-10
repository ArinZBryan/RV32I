from bitint import Bitint
from cocotb.types import LogicArray, Range
import pytest

def test_bitint_construction():
    # Unsigned Values
    assert Bitint(0, 8, False).to_unsigned() == 0
    assert Bitint(255, 8, False).to_unsigned() == 255
    with pytest.raises(Exception):
        Bitint(256, 8, False)
    with pytest.raises(Exception):
        Bitint(-1, 8, False)
        
    # 2's complement values
    assert Bitint(-128, 8, True).to_signed() == -128
    assert Bitint(-1, 8, True).to_signed() == -1
    assert Bitint(0, 8, True).to_signed() == 0
    assert Bitint(127, 8, True).to_signed() == 127
    with pytest.raises(Exception):
        Bitint(255, 8, True)
    with pytest.raises(Exception):
        Bitint(128, 8, True)
    
def test_bitint_addition():
    assert Bitint(100, 8, False) + Bitint(200, 8, False) == 44
    assert Bitint(127, 8, True) + Bitint(1, 8, True) == -128
    assert Bitint(-1, 8, True) + Bitint(1, 8, True) == 0
    assert Bitint(0, 8, False) + Bitint(0, 8, False) == 0
    assert Bitint(255, 8, False) + Bitint(1, 8, False) == 0
    
def test_bitint_subtraction_negation():
    assert Bitint(5, 8, False) - Bitint(3, 8, False) == 2
    assert Bitint(0, 8, False) - Bitint(1, 8, False) == 255
    assert Bitint(-128, 8, True) - Bitint(1, 8, True) == 127
    assert Bitint(50, 8, True) - Bitint(100, 8, True) == -50
    assert -Bitint(1, 8, True) == -1
    assert -Bitint(-1, 8, True) == 1
    assert -Bitint(-128, 8, True) == -128
    assert abs(Bitint(-5, 8, True)) == 5
    assert abs(Bitint(5, 8, True)) == 5
    
def test_bitint_lshl():
    assert Bitint(1, 8, False) << 1 == 2
    assert Bitint(0x80, 8, False) << 1 == 0
    assert Bitint(0xff, 8, False) << 0 == 0xff
    assert Bitint(1, 8, False) << 7 == 128
    assert (Bitint(-1, 8, True) << 1).to_unsigned() == 0xfe
    assert Bitint(3, 4, False) << 2 == 12
    
def test_bitint_lshr():
    assert Bitint(0x80, 8, False).lshr(1) == 0x40
    assert Bitint(0xff, 8, False).lshr(4) == 0x0f
    assert Bitint(1, 8, False).lshr(1) == 0
    assert Bitint(1, 8, False).lshr(8) == 0
    assert Bitint(-1, 8, True).lshr(1).bits == 0x7f 
    assert Bitint(200, 8, False) >> 2 == 200 >> 2
    
def test_bitint_ashr():
    assert Bitint(64, 8, True) >> 1 == 32
    assert (Bitint(64, 8, True) >> 1).bits == 0x20
    assert Bitint(-1, 8, True) >> 1 == -1
    assert Bitint(-1, 8, True) >> 7 == -1
    assert Bitint(-128, 8, True) >> 1 == -64
    assert Bitint(-128, 8, True) >> 7 == -1
    assert Bitint(-4, 8, True) >> 1 == -2
    assert Bitint(-128, 8, True) >> 8 == -1
    assert Bitint(0x80, 8, False) >> 1 == 0x40