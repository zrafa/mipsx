CC=mipsel-linux-gcc

CFLAGS=-Wall -g

.PHONY:		all clean spotless

all:
	mipsel-linux-as  -g --gstabs -o uartmips.o uartmips.s 
	mipsel-linux-gcc -g -c -o init.o init.c 
	mipsel-linux-gcc  -o uartmips uartmips.o init.o 


clean:
		rm -f uartmips init.o uartmips.o

