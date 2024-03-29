
/*
 * uart-mips : ejemplo de programa en lenguaje ensamblador MIPS para
 * acceder a los registros uart de la placa SIE, y realizar E/S.
 *
 * Copyright (C) 2014 Rafael Ignacio Zurita <rafa@fi.uncoma.edu.ar>
 *
 *   mipsx and examples are free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version. Check COPYING file.
 */
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/mman.h>

#define UART_BASE		0x10032000
#define PDFUNS_REGISTER		0x10010344


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

	printf("UART Line Status Register = %0x\n", (*(volatile uint32_t *) (uart_reg_base+(20))));
	/* mem = 3; */

}

void uartmips_exit(void) {

	printf("mem=%i\n", uart_reg_base);
	exit(0);
}

void uartmips_printf(void) {

//	printf("UART Interrupt Enable Register = %0x\n", (*(volatile uint32_t *) (uart_reg_base+(4))));
	uint32_t valor = (*(volatile uint32_t *) (uart_reg_base+(8)));
	printf("UART FIFO Control Register = %0x\n", valor );
//	printf("UART Line Status Register = %0x\n", (*(volatile uint32_t *) (uart_reg_base+(20))));
//	printf("UART Line Control Register = %0x\n", (*(volatile uint32_t *) (uart_reg_base+(12))));
	return;
}
