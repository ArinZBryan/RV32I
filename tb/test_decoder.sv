import types::*;
module test_decoder ();

types::raw_instruction_t Raw;
types::instruction_t Decoded;

decoder d(.Raw(Raw), .Decoded(Decoded));
endmodule
