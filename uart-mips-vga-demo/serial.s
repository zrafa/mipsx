
                .data
.global uart_reg_base
.globl uart_reg_base
uart_reg_base:  .word 0
mensaje:		.asciiz "Hola Mundo"

.text
.globl main
main:
        jal uartmips_init

	li $t5, 0xFFFFFF00   # Para "limpiar" el primer byte del TX DATA


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
	bne $a0, $0, recorrer_mensaje
	
# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall



enviar_char:

espera_tx:
	lw	$2,0($t0)
	andi	$2,$2,0x200
	beq	$2, $0, espera_tx

	and	$2, $2, $t5
	or	$2, $2, $a0
	sw	$2,0($t0)

	jr	$ra



