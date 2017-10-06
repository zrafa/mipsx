
                .data
.global uart_reg_base
.globl uart_reg_base
uart_reg_base:  .word 0
mensaje:	.byte 27, 27
		.ascii "\r\n ** Microcomputer **"
		.ascii " **      MIPS     **" 
		.asciiz "ar9331 SOC 32MB RAM\r\nREADY.\r\n"

.text
.globl main
main:
        jal uartmips_init



	# Cargamos t0 con la direrccion del registro base del uart
        la $t0, uart_reg_base
        lw $t0, 0($t0)

	# Ponemos en cero el bit de registro de habilitacion de interrupciones
	li $t1, 0
	sw $t1, 0x10($t0)



mostrar_bienvenida:
	la  $t4, mensaje
	lb  $a0, ($t4)
recorrer_mensaje:
	jal enviar_char
	addi $t4, $t4, 1
	lb  $a0, ($t4)

	li $t3, 0
	delay:
		addi $t3, $t3, 1
		bne $t3, 1000000, delay
	bne $a0, $0, recorrer_mensaje
	

eco:
	jal obtener_tecla
	move $a0, $v0
	jal enviar_char
	j eco


# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall



enviar_char:
	# Cargamos t0 con la direrccion del registro base del uart
        la $t0, uart_reg_base
        lw $t0, 0($t0)

espera_tx:
	lw	$t2,0($t0)
	andi	$t2,$t2,0x200
	beq	$t2, $0, espera_tx

	li $t5, 0xFFFFFF00   # Para "limpiar" el primer byte del TX DATA
	and	$t2, $t2, $t5
	or	$t2, $t2, $a0
	sw	$t2,0($t0)

	jr	$ra




obtener_tecla:
	# Cargamos t0 con la direrccion del registro base del uart
        la $t0, uart_reg_base
        lw $t0, 0($t0)
espera_rx:
	lw	$t2,0($t0)
	andi	$t2,$t2,0x100
	beq	$t2, $0, espera_rx
	ori	$t2,$t2,0x100
	sw	$t2,0($t0)
espera_rx2:
	lw	$t2,0($t0)
	andi	$t2,$t2,0x100
	beq	$t2, $0, espera_rx2
	lw	$t2,0($t0)
	# lw	$t2,0($t0)

	# lw	$t2,0($t0)
	li $t5, 0x000000FF # Para "limpiar" los primeros 3 bytes de RX TX DATA
	and	$t2, $t2, $t5
	move	$v0, $t2

	jr	$ra


