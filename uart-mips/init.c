#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/mman.h>

#define UART_BASE		0x10030000


#define PAGE_SIZE 4096


extern volatile void *uart_reg_base;

static void die(int sig)
{
	_exit(0);
}

void uartmips_init(void) {

	int fd;

	fd = open("/dev/mem", O_RDWR | O_SYNC);
        if (fd < 0) {
		perror("/dev/mem");
		exit(1);
	}
	uart_reg_base = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd,
	    UART_BASE);
	if (uart_reg_base == MAP_FAILED) {
		perror("mmap");
		exit(1);
	}

	/* mem = 3; */

}

void uartmips_exit(void) {

	printf("mem=%i\n", uart_reg_base);
}
