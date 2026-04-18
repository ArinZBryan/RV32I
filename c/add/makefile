OBJCOPY=riscv32-unknown-elf-objcopy
CC=riscv32-unknown-elf-gcc
CFLAGS=-march=rv32i -mabi=ilp32 -ffreestanding -nostdlib -nostartfiles -O0 -g
AFLAGS=-march=rv32i -mabi=ilp32
LDFLAGS=-march=rv32i -mabi=ilp32 -nostdlib -nostartfiles

bin: program.elf
	$(OBJCOPY) -O binary program.elf program.bin

main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o

start.o: start.s
	$(CC) $(AFLAGS) -c start.s -o start.o

program.elf: main.o start.o
	$(CC) $(LDFLAGS) -T link.ld start.o main.o -o program.elf

