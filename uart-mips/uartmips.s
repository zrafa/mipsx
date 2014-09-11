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
	beq $t2, $zero, listo

	li $t3, 0x4c		# 0x4c es la 'L' en ascii
	sw $t3, 0($t0)

	jal uartmips_exit

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


