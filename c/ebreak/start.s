.section .text.start
.global _start

_start:
    la   sp, __stack_top  # Setup the stack pointer to the top of the stack. It grows down.
    la   t0, __bss_start  # Load the start and end addresses for the uninitialised static variables
    la   t1, __bss_end
bss_loop:                 # This is a for loop, that manually sets every value between __bss_start
    bge  t0, t1, bss_done # __bss_end to zero. Since C does not have default constructors, this should
    sw   zero, 0(t0)      # be fine.
    addi t0, t0, 4
    j    bss_loop
bss_done:

    # Use x31 as a sentinel address. we set it to zero before main and then one afterwards
    # I should be able to detect this in cocotb, and move to viewing result early if it did
    li   x31, 0
    call main
    li   x31, 1

halt:
    j halt # I should only be running for a fixed number of cycles, so if we somehow get here without
           # detecting the x31, then the simulation should die. Eventually.
