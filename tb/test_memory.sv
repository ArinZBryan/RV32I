import types::*;

module test_memory();

logic clock;

// Port A
types::word_t portA_addr;
types::word_t portA_writeval;
types::word_t portA_memval;
types::byte_select_t portA_write_enable;

types::word_t portB_addr;
types::word_t portB_writeval;
types::word_t portB_memval;
types::byte_select_t portB_write_enable;

memory mem (
    .clk(clock),
    .portA_addr(portA_addr), .portB_addr(portB_addr),
    .portA_writeval(portA_writeval), .portB_writeval(portB_writeval),
    .portA_write_enable(portA_write_enable), .portB_write_enable(portB_write_enable),
    .portA_memval(portA_memval), .portB_memval(portB_memval)
);

endmodule
