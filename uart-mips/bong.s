
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
paletas:	.word 5, 5

bienvenida:	.asciiz "Hola mundo en MIPS - Placa electronica SIE XBurst CPU MIPS32v2"
tecla:		.word 0


		.text
		.global main

main:

	jal uartmips_init
	la $t0, uart_reg_base
	lw $t0, 0($t0)

	jal secuencia_de_escape
	jal mover_cursor_1_1

	jal secuencia_de_escape
	jal limpiar_pantalla
	jal imprimir_bienvenida

bucle:
	jal detectar_entrada
	jal analizar_tecla

	jal secuencia_de_escape
	jal mover_cursor_1_1

#	jal secuencia_de_escape
#	jal limpiar_pantalla

#	jal secuencia_de_escape
#	jal reverso

	
	jal secuencia_de_escape
	jal mover_paleta_anterior
	jal pintar_paleta_espacio

	jal secuencia_de_escape
	jal mover_paleta
	jal pintar_paleta

	jal dormir
	#jal imprimir_caracter

	#jal imprimir_caracter

	# jal uartmips_exit
	j bucle


dormir:
	li $t3, 0xFFFFF
repetir:
	addi $t3, $t3, -1
	bne $t3, $zero, repetir
	jr $ra

secuencia_de_escape:
	li $t3, 0x1B
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	li $t3, 0x5b
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra

reverso:
	# ESC[7m
	li $t3, 0x37
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	li $t3, 0x6d
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	jr $ra

quitarreverso:
	# ESC[(0
	li $t3, 0x28
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	li $t3, 0x30
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra


detectar_entrada:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x1	# 0x01 es el bit de TEMP

	# verificamos si hay entrada
	beq $t2, $zero, no_hay_entrada
	# si se ha presionado una tecla
	lw $t3, 0($t0)
	sw $t3, tecla
	jr $ra
no_hay_entrada:
	sw $zero, tecla
	jr $ra

analizar_tecla:
	lw $t1, tecla
	beq $t1, $zero, salir_analizar_tecla

	addi $t2, $t1, -0x61
	beq $t2, $zero, tecla_a

	addi $t2, $t1, -0x7a
	beq $t2, $zero, tecla_z

	jr $ra
tecla_a:
	lw $t1, paletas
	beq $t1, $zero, salir_analizar_tecla
	sw $t1, paletas+4
	addi $t1, $t1, -1
	sw $t1, paletas
	jr $ra

tecla_z:
	lw $t1, paletas
	li $t2, 0xA
	beq $t1, $t2, salir_analizar_tecla
	sw $t1, paletas+4
	addi $t1, $t1, 1
	sw $t1, paletas
	jr $ra

	
# 0x61 es 'a'
# 0x7a es 'z'
salir_analizar_tecla:
	jr $ra
	
limpiar_pantalla:
	li $t3, 0x4A
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra
	

mover_paleta:

	li $t3, 0x31
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	lw $t3, paletas
	addi $t3, $t3, 0x30
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	jr $ra

mover_paleta_anterior:

	li $t3, 0x31
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	lw $t3, paletas+4
	addi $t3, $t3, 0x30
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	jr $ra


pintar_paleta_espacio:
	li $t3, 0x3b
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	li $t3, 0x48
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	# Dibujamos un espacio en reverso
	li $t3, 0x20
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra
	
pintar_paleta:
	li $t3, 0x3b
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	li $t3, 0x48
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	
	# Dibujamos un espacio en reverso
	li $t3, 0x40
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra
	
mover_cursor_1_1:
	li $t3, 0x3b
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	li $t3, 0x48
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra

imprimir_bienvenida:
	la $t4, bienvenida

bucle_imprimir_bienvenida:
	lb $t3, ($t4)
	add $t6, $ra, 0
	jal imprimir_caracter
	add $ra, $t6, 0
	addi $t4, $t4, 1
	bne $t3, $zero, bucle_imprimir_bienvenida

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

# Esperamos a que el serial nos indique que podemos escribir
esperaentrada:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x1	# 0x01 es el bit de TEMP
	beq $t2, $zero, esperaentrada
	jr $ra

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


