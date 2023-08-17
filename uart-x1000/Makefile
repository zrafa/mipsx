CC=mips-linux-gnu-gcc

CFLAGS=-Wall -g

.PHONY:		all clean spotless

all:
	# mips-linux-gnu-as  -g --gstabs -o uartmips.o uartmips.s 
	# mips-linux-gnu-as  -g --gstabs -o bong.o bong.s 
	# mips-linux-gnu-as  -g --gstabs -o hello.o hello.s 
	# mips-linux-gnu-gcc -g -c -o uartmips_init.o uartmips_init.c 
	mips-linux-gnu-gcc -c uartmips.s 
	mips-linux-gnu-gcc -c bong.s 
	mips-linux-gnu-gcc -c hello.s 
	mips-linux-gnu-gcc -c uartmips_init.c 
	mips-linux-gnu-gcc  -o uartmips uartmips.o uartmips_init.o 
	mips-linux-gnu-gcc  -o bong bong.o uartmips_init.o 
	mips-linux-gnu-gcc  -o hello hello.o uartmips_init.o 


clean:
		rm -f uartmips uartmips_init.o uartmips.o bong bong.o

