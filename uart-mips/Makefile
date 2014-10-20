CC=mipsel-linux-gcc

CFLAGS=-Wall -g

.PHONY:		all clean spotless

all:
	mipsel-linux-as  -g --gstabs -o uartmips.o uartmips.s 
	mipsel-linux-as  -g --gstabs -o bong.o bong.s 
	mipsel-linux-as  -g --gstabs -o hello.o hello.s 
	mipsel-linux-gcc -g -c -o uartmips_init.o uartmips_init.c 
	mipsel-linux-gcc  -o uartmips uartmips.o uartmips_init.o 
	mipsel-linux-gcc  -o bong bong.o uartmips_init.o 
	mipsel-linux-gcc  -o hello hello.o uartmips_init.o 


clean:
		rm -f uartmips uartmips_init.o uartmips.o bong bong.o

