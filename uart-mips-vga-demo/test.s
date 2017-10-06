
                .data
.global uart_reg_base
.globl uart_reg_base
uart_reg_base:  .word 0
letras:		.asciiz "Hola Mundo"

.text
.globl main
main:
        jal uartmips_init

	li $t5, 0xFFFFFF00
	lb  $t4, letras
        la $t0, uart_reg_base
        lw $t0, 0($t0)

	li $t1, 0
	sw $t1, 0x10($t0)
$L2:
	lw	$2,0($t0)
	andi	$3,$2,0x200
	beq	$3,$0,$L2
	
	and	$2, $2, $t5
	or	$2, $2, $t4
	sw	$2,0($t0)

$espera:
	lw	$2,0($t0)
	andi	$2,$2,0x200
	beq	$2,$0,$espera



# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall







