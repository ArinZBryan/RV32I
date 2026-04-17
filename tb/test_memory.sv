import types::*;

module test_memory();

logic clock;

// Port A
types::word_t PortA_Addr;
types::word_t PortA_WData;
types::word_t PortA_Out;
types::byte_select_t PortA_WriteSelect;

types::word_t PortB_Addr;
types::word_t PortB_WData;
types::word_t PortB_Out;
types::byte_select_t PortB_WriteSelect;

memory mem (
    .clock(clock),
    .PortA_Addr(PortA_Addr),               .PortB_Addr(PortB_Addr),
    .PortA_WData(PortA_WData),             .PortB_WData(PortB_WData),
    .PortA_WriteSelect(PortA_WriteSelect), .PortB_WriteSelect(PortB_WriteSelect),
    .PortA_Out(PortA_Out),                 .PortB_Out(PortB_Out)
);

endmodule
