
| `funct3` | R-type    | I-type            | S-type        | B-type   |
| -------: | --------- | ----------------- | ------------- | -------- |
| 0        | ADD/SUB   | ADD/Load8         | Store8 (ADD)  | BEQ/XOR  |
| 1        | LSHL      | LSHL/Load16       | Store16 (ADD) | BNEQ/XOR |
| 2        | SLT       | SLT/Load32        | Store32 (ADD) | Unused   |
| 3        | SLTU      | SLTU              | Unused        | Unused   |
| 4        | XOR       | XOR/Loadu8        | Unused        | BLT/SUB  |
| 5        | LSHR/ASHR | LSHR/ASHR/Loadu16 | Unused        | BGE/SUB  |
| 6        | OR        | OR                | Unused        | BLTU/SUB |
| 7        | AND       | AND               | Unused        | BGEU/SUB |


Notes:
- R/I type instructions have the same funct3 decode logic
- ALU modifier comes directly from bit 30 of the instruction
- Sign extensions always extend from bit 31 of the instruction
- S/I (Load) instructions use the same first two bits of funct3
- I (Load) instructions use bit2 of funct3 as the unsigned toggle bit
- After ALU, place load/store unit that either takes the ALU output
  as an address or places passes it through to registers
- After ALU, place branch condition unit (evaluates branches based on funct3 and ALU output)


ALU Opcodes:
- ALU_ADD = 0, ALU_SHL = 1, ALU_SLT = 2, ALU_SLTU = 3, ALU_XOR = 4, ALU_SHR = 5, ALU_OR = 6, ALU_AND = 7
- hardwire I (load) to ALU_ADD
- hardwire S to ALU_ADD
- hardwire B to ALU_SLT/ALU_SLTU