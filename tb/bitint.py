from cocotb.types import LogicArray, Range

class Bitint():
    def __init__(self, pyint: int, nbits: int, signed: bool):
        if not Bitint.representable(pyint, nbits, signed):
            raise ArithmeticError(f"Number ({pyint}) not representable in the specified format {"s" if signed else "u"}{nbits}")
        self.signed = signed
        self.size = nbits
        self.signbitmask = 1 << (nbits - 1)
        self.numbitmask = (1 << nbits) - 1
        self.bits = pyint & self.numbitmask
    
    @staticmethod
    def representable(pyint: int, nbits: int, signed: bool):
        """Returns whether the python integer is representable as a `nbits`-bit signed/unsigned number"""
        if signed:
            if pyint < (-(2**(nbits - 1))):
                return False
            elif pyint > (2**(nbits-1) - 1):
                return False
            else:
                return True
        else:
            if pyint < 0:
                return False
            elif pyint >= 2**nbits:
                return False
            else:
                return True
    @staticmethod
    def maxvalue(nbits: int, signed: bool) -> int:
        if signed:
            return (2**(nbits-1) - 1)
        else:
            return (2**nbits) - 1
    @staticmethod
    def minvalue(nbits: int, signed: bool) -> int:
        if signed:
            return (-(2**(nbits - 1)))
        else:
            return 0
    
    def __add__(self, other : "Bitint | int") -> "Bitint":
        if isinstance(other, int):
            return self + Bitint(other, self.size, self.signed)
        truevalue = self.bits + other.bits
        return Bitint._coerce(truevalue, self.size, self.signed)
    
    def __sub__(self, other : "Bitint | int") -> "Bitint":
        if isinstance(other, int):
            return self - Bitint(other, self.size, self.signed)
        truevalue = self.bits - other.bits
        return Bitint._coerce(truevalue, self.size, self.signed)

    def __neg__(self) -> "Bitint":
        return Bitint._coerce(-self.bits, self.size, self.signed)          
    
    def lshl(self, other : "Bitint | int") -> "Bitint":
        if other < 0:
            raise ValueError("Shift only valid for non-negative integers")
        if isinstance(other, int):
            return self << Bitint(other, self.size, self.signed)
        return Bitint._coerce((self.bits << other.bits) & self.numbitmask, self.size, self.signed)
        
    def __lshift__(self, other : "Bitint | int") -> "Bitint":
        return self.lshl(other)
        
    def ashr(self, other : "Bitint | int") -> "Bitint":
        if other < 0:
            raise ValueError("Shift only valid for non-negative integers")
        if isinstance(other, int):
            return self >> Bitint(other, self.size, self.signed)
        if self.signed:
            fill_bits = min(other.bits, self.size)
            fill_mask = (self.numbitmask) & (~((1 << (self.size - fill_bits)) - 1))
            filled_bits = (-1 if (self.bits & self.signbitmask) else 0) & fill_mask
            return Bitint._coerce(self.bits >> other.bits | filled_bits, self.size, self.signed)
        else:
            return self.lshr(other)

    def __rshift__(self, other : "Bitint | int") -> "Bitint":
        return self.ashr(other)
    
    def lshr(self, other : "Bitint | int") -> "Bitint":
        if other < 0:
            raise ValueError("Shift only valid for non-negative integers")
        if isinstance(other, int):
            return self.lshr(Bitint(other, self.size, self.signed))
        return Bitint._coerce(self.numbitmask & self.bits >> other.bits, self.size, self.signed)
            
    def __and__(self, other : "Bitint | int") -> "Bitint":
        if isinstance(other, int):
            return self & Bitint(other, self.size, self.signed)
        return Bitint._coerce(self.bits & other.bits, self.size, self.signed)
    
    def __or__(self, other : "Bitint | int") -> "Bitint":
        if isinstance(other, int):
            return self | Bitint(other, self.size, self.signed)
        return Bitint._coerce(self.bits | other.bits, self.size, self.signed)
    
    def __xor__(self, other : "Bitint | int") -> "Bitint":
        if isinstance(other, int):
            return self ^ Bitint(other, self.size, self.signed)
        return Bitint._coerce(self.bits ^ other.bits, self.size, self.signed)

    def __lt__(self, other : "Bitint | int") -> bool:
        if isinstance(other, int):
            return self < Bitint(other, self.size, self.signed)
        if self.signed:
            return self.to_signed() < other.to_signed()
        else:
            return self.bits < other.bits
    
    def __le__(self, other : "Bitint | int") -> bool:
        if isinstance(other, int):
            return self <= Bitint(other, self.size, self.signed)
        return self < other or self == other
    
    def __gt__(self, other : "Bitint | int") -> bool:
        if isinstance(other, int):
            return self > Bitint(other, self.size, self.signed)
        if self.signed:
            return self.to_signed() < other.to_signed()
        else:
            return self.bits < other.bits
    
    def __ge__(self, other : "Bitint | int") -> bool:
        if isinstance(other, int):
            return self >= Bitint(other, self.size, self.signed)
        return self > other or self == other

    def __eq__(self, other : "Bitint | int") -> bool:
        if isinstance(other, int):
            return self == Bitint(other, self.size, self.signed)
        return self.bits == other.bits and self.signed == other.signed

    def __abs__(self) -> "Bitint":
        if self.signed:
            if self < 0:
                return -self
            else:
                return self
        else:
            return self
        
    def __repr__(self) -> str:
        return f"{"s" if self.signed else "u"}{self.size}{self.bits:0{self.size}b}"
    
    def bin(self) -> str:
        return self.__repr__()
    
    def hex(self) -> str:
        hex_digits = (self.size + 3) // 4
        return f"{"s" if self.signed else "u"}{self.size}x{self.bits:0{hex_digits}X}"
    
    def __hash__(self) -> int:
        return hash((self.bits, self.size, self.signed))
        
    @staticmethod
    def _coerce(pyint: int, nbits: int, signed: bool) -> "Bitint":
        new_item = Bitint.__new__(Bitint)
        new_item.signed = signed
        new_item.size = nbits
        new_item.signbitmask = 1 << (nbits - 1)
        new_item.numbitmask = (1 << nbits) - 1
        new_item.bits = pyint & new_item.numbitmask
        return new_item

    def zeroextend(self, nbits: int) -> "Bitint":
        if nbits < self.size:
            raise ValueError("Cannot extend to size smaller than current size")
        return Bitint._coerce(self.bits, nbits, self.signed)

    def signextend(self, nbits: int) -> "Bitint":
        if nbits < self.size:
            raise ValueError("Cannot extend to size smaller than current size")
        if not self.signed:
            return self.zeroextend(nbits)
        else:
            fill_bits = nbits - self.size
            fill_mask = ((1 << nbits)-1) & (~((1 << (nbits - fill_bits)) - 1))
            filled_bits = (-1 if (self.bits & (1 << (self.size-1))) else 0) & fill_mask
            return Bitint._coerce(self.bits | filled_bits, nbits, self.signed)
            
    def to_unsigned(self) -> int:
        return self.bits
    
    def to_signed(self) -> int:
        value = self.bits
        if self.bits >= self.signbitmask:
            value -= 2 * self.signbitmask
        return value
    
    def to_logicarray(self) -> LogicArray:
        return LogicArray(self.bits, Range(self.size - 1, 'downto', 0))
    
if __name__ == "__main__":
    a = Bitint(-1, 32, True)
    b = Bitint(2, 32, True)
    a.zeroextend(33).lshl(b.zeroextend(33) & 0b11111)