math: main.asm
	nasm -f elf32 main.asm -o tmp.o
	ld -m elf_i386 tmp.o -o math
	rm tmp.o

clean:
	rm -f tmp.o math

PHONY: clean