import types::*;
module test_decoder ();

types::raw_instruction_t raw;
types::instruction_t decoded;

decoder d(.raw(raw), .decoded(decoded));
endmodule
