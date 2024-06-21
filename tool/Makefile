all:	boilerplate.c fuzz.S	
	@nasm -f elf64 fuzz.S -o fuzz.o
	@gcc boilerplate.c -o fuzz -mavx -mavx2 -msse -mssse3 -mbmi2 -maes -msse3 fuzz.o
	@sudo ./fuzz $(MSR_ADDR) $(MSR_NAME) 2>/dev/null

clean:
	@rm -f fuzz fuzz.o
