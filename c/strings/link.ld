ENTRY(_start)

MEMORY
{
    MEM (rwx) : ORIGIN = 0x00000000, LENGTH = 1K
}

SECTIONS
{
    .text : {
        *(.text.start)  /* PC entrypoint is 0, so the program must start there */
        *(.text*)
    } > MEM

    .bss : {
        __bss_start = .;
        *(.bss*)
        __bss_end = .;
    } > MEM

    .data : {
        *(.data*)
    } > MEM

    .rodata : {
        *(.rodata*)
    } > MEM

    . = ALIGN(4);
    __stack_top = ORIGIN(MEM) + LENGTH(MEM);  /* stack grows down from top */
}