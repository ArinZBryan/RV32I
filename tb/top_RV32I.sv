module top_RV32I();

logic clock;
logic _reset;

RV32I rv32i (.clock(clock), ._reset(_reset));

endmodule;
