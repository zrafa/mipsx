
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
paletas:	.byte 0, 0

cadena:		.asciiz "Hola mundo"
tecla:		.byte 0


		.text
		.global main

main:

	jal uartmips_init	# Mapeamos los registors del uart de la SIE a esta direccion
	la $t0, uart_reg_base	# Cargamos el puntero con la direccion del primer registro uart
	lw $t0, 0($t0)		# Cargamos la direccion en memoria del primer registro uart

	la $t4, cadena



imprimir_cadena:
	lb $t3, ($t4)

# Esperamos a que el uart nos indique que podemos escribir
esperalisto:
	lw $t1, ($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x200	# 0x40 es el bit de TEMP
	beq $t2, $zero, esperalisto
	jr $ra

	sw $t3, 0($t0)		# Escribimos el caracter en el registro de transmicion


	addi $t4, $t4, 1
	bne $t3, $zero, imprimir_cadena

	jal uartmips_exit




# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


