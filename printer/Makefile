printer: printer.asm
	nasm -f elf32 printer.asm -o printer.o
	ld -m elf_i386 printer.o -o printer
	rm printer.o
