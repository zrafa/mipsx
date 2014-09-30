
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
pelota:		.word 0
mover_pelota:	.word 1

bienvenida:	.asciiz "Hola mundo en MIPS - Placa electronica SIE XBurst CPU MIPS32v2"
tecla:		.word 0

limpiar_pantalla:	.byte 0x1B, 0x5B, 0x32, 0x4A, 0x00
cursor_10_1:	.byte 0x1B, 0x5B, 0x31, 0x30, 0x3B, 0x48, 0x00
cursor_10_10:	.byte 0x1B, 0x5B, 0x31, 0x3B, 0x38, 0x30, 0x48, 0x00
reverso:	.byte 0x1B, 0x5B, 0x37, 0x6D, 0x00
quitar_reverso:	.byte 0x1B, 0x5B, 0x30, 0x6D, 0x00
fin_seq_esc_mover:	.byte 0x3B, 0x48, 0x00

		.text
		.global main

main:

	jal uartmips_init
	la $t0, uart_reg_base
	lw $t0, 0($t0)


	jal enviar_limpiar_pantalla
	jal mover_cursor_10_1
	jal imprimir_bienvenida

bucle:
	jal detectar_entrada
	jal analizar_tecla


	jal reverso_off

	jal secuencia_de_escape
	jal mover_paleta_anterior
	jal enviar_fin_seq_esc_mover
	jal pintar_paleta_espacio

	jal reverso_on
	jal secuencia_de_escape
	jal mover_paleta
	jal enviar_fin_seq_esc_mover
	jal pintar_paleta



# 	jal secuencia_de_escape
# 	jal reverso_off

	# jal mover_cursor_10_10

	jal dormir
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

reverso_on:
	# ESC[7m
	la $t4, reverso
	add $s0, $ra, 0
	jal bucle_imprimir
	add $ra, $s0, 0
	jr $ra

reverso_off:
	# ESC[0m
	la $t4, quitar_reverso
	add $s0, $ra, 0
	jal bucle_imprimir
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
	li $t2, 0x9
	beq $t1, $t2, salir_analizar_tecla
	sw $t1, paletas+4
	addi $t1, $t1, 1
	sw $t1, paletas
	jr $ra

	
# 0x61 es 'a'
# 0x7a es 'z'
salir_analizar_tecla:
	jr $ra
	
enviar_limpiar_pantalla:
	la $t4, limpiar_pantalla
	add $s0, $ra, 0
	jal bucle_imprimir
	add $ra, $s0, 0
	jr $ra
	

mover_paleta:
	lw $t3, paletas
	addi $t3, $t3, 0x30
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	jr $ra

mover_paleta_anterior:
	lw $t3, paletas+4
	addi $t3, $t3, 0x30
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0

	jr $ra


pintar_paleta_espacio:
	# Dibujamos un espacio en reverso
	li $t3, 0x20
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra
	
enviar_fin_seq_esc_mover:
	la $t4, fin_seq_esc_mover
	add $s0, $ra, 0
	jal bucle_imprimir
	add $ra, $s0, 0
	jr $ra

pintar_paleta:
	
	# Dibujamos un espacio en reverso
	li $t3, 0x40
	add $s0, $ra, 0
	jal imprimir_caracter
	add $ra, $s0, 0
	jr $ra
	
mover_cursor_10_10:
	la $t4, cursor_10_10
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

# Esperamos a que el serial nos indique que podemos leer
esperaentrada:
	lw $t1, 0x14($t0)	# reg_base + 0x14 es registro status en jz4740
	andi $t2, $t1, 0x1	# 0x01 es el bit de TEMP para conocer si existe una entrada
	beq $t2, $zero, esperaentrada
	jr $ra

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


