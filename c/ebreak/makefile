OBJCOPY=riscv32-unknown-elf-objcopy
OBJDUMP=riscv32-unknown-elf-objdump
CC=riscv32-unknown-elf-gcc
CFLAGS=-march=rv32i -mabi=ilp32 -ffreestanding -nostdlib -nostartfiles -O0 -g
AFLAGS=-march=rv32i -mabi=ilp32
LDFLAGS=-march=rv32i -mabi=ilp32 -nostdlib -nostartfiles

.PHONY: clean

bin: program.elf
	$(OBJCOPY) -O binary program.elf program.bin

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

start.o: start.s
	$(CC) $(AFLAGS) -c start.s -o start.o

program.elf: main.o start.o
	$(CC) $(LDFLAGS) -T link.ld start.o main.o -o program.elf

clean:
	rm program.bin program.elf main.o start.o objdump.txt

objdump: program.elf
	$(OBJDUMP) -d program.elf > objdump.txt