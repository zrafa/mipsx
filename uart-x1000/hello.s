
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


bienvenida:	.asciiz "Hola mundo en MIPS - Placa electronica HALLEY2 CPU MIPS32v2"



		.text
		.global main

main:

	jal uartmips_init
	la $t0, uart_reg_base
	lw $t0, 0($t0)
	sw $zero, 4($t0)
	

imprimir_bienvenida:
	la $t4, bienvenida

bucle_imprimir:
	lb $t3, ($t4)
listo:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x40	# 0x40 es el bit de TEMP
	beq $t2, $zero, listo
	
	sw $t3, 0($t0)
	addi $t4,$t4,1 
	bne $t3, $zero, bucle_imprimir

espera_entrada:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x01	# 0x40 es el bit de TEMP
	beq $t2, $zero, espera_entrada
	lb $t3, 0($t0)
listo2:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x40	# 0x40 es el bit de TEMP
	beq $t2, $zero, listo2
	addi $t3, $t3, 1
	sw $t3, 0($t0)

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


