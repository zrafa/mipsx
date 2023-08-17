
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

bienvenida:	.asciiz "Hola mundo en placa Ingenic Halley2 XBurst MIPS 1Ghz - MIPS32v2"
tecla:		.word 0

limpiar_pantalla:	.byte 0x1B, 0x5B, 0x32, 0x4A, 0x00
cursor_10_1:	.byte 0x1B, 0x5B, 0x31, 0x30, 0x3B, 0x48, 0x00
cursor_10_10:	.byte 0x1B, 0x5B, 0x31, 0x3B, 0x38, 0x30, 0x48, 0x00
reverso:	.byte 0x1B, 0x5B, 0x37, 0x6D, 0x00
quitar_reverso:	.byte 0x1B, 0x5B, 0x30, 0x6D, 0x00
fin_seq_esc_mover:	.byte 0x3B, 0x48, 0x00

		.text
		.global main

	
enviar_limpiar_pantalla:
	la $t4, limpiar_pantalla
	add $s0, $ra, 0
	jal bucle_imprimir
	add $ra, $s0, 0
	jr $ra
	

	

mover_cursor_10_1:
	la $t4, cursor_10_1
	add $s0, $ra, 0
	jal bucle_imprimir
	add $ra, $s0, 0
	jr $ra

imprimir_bienvenida:
	la $t4, bienvenida

bucle_imprimir:
	lb $t3, ($t4)
	add $t6, $ra, 0
	jal imprimir_caracter
	add $ra, $t6, 0
	addi $t4, $t4, 1
	bne $t3, $zero, bucle_imprimir

	#jal uartmips_exit
	jr $ra

# Imprimir caracter
imprimir_caracter:
	add $t7, $ra, 0
	jal listo
	add $ra, $t7, 0
	sw $t3, 0($t0)
	jr $ra


# Esperamos a que el serial nos indique que podemos escribir
listo:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x40	# 0x40 es el bit de TEMP
	beq $t2, $zero, listo
	jr $ra
main:

	add $s2, $ra, 0
	jal uartmips_init
	la $t0, uart_reg_base
	lw $t0, 0($t0)


	jal enviar_limpiar_pantalla
	jal mover_cursor_10_1
	jal imprimir_bienvenida



 
detectar_entrada:
        lw $t1, 0x14($t0)       # reg_base + 0x14 es registro status en jz4740
        andi $t2, $t1, 0x1      # 0x01 es el bit de TEMP

        # verificamos si hay entrada
        beq $t2, $zero, detectar_entrada 
        # si se ha presionado una tecla
        lw $t3, 0($t0)
	jal imprimir_caracter
	j detectar_entrada


	add $ra, $s2, 0

	jr $ra

