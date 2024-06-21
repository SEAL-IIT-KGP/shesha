all: leak perfmon
	
FLAGS:=-DSTRIDE=0x400 -DSTRIDE_LOG=10 -DLEAK_SIZE=256 -DLEAK_SIZE_LOG=8 -DITER=1000

leak: leak.c fp.S
	nasm -f elf64 fp.S -o fp.o -I ./common $(FLAGS)
	gcc -g leak.c -o leak fp.o -I ./common -no-pie $(FLAGS)

perfmon: perfmon.c fuzz.S
	nasm -f elf64 fuzz.S -o fuzz.o
	gcc perfmon.c -o fuzz -masm=intel -mavx -mavx2 -msse -mssse3 -mbmi2 -maes -msse3 fuzz.o

clean:
	rm -f leak fp.o fuzz.o fuzz
