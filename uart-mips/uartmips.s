
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

.global uart_reg_base

		.data
uart_reg_base:	.word 0


		.text
		.global main

main:

	jal uartmips_init
	la $t0, uart_reg_base
	lw $t0, 0($t0)

# Esperamos a que el serial nos indique que podemos escribir
listo:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t1, $t1, 0x40	# 0x40 es el bit de TEMP
	beq $t1, $zero, listo

	li $t3, 0x4c		# 0x4c es la 'L' en ascii
	sw $t3, 0($t0)

	jal uartmips_exit

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


