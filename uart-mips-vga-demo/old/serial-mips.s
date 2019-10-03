
                .data
.global uart_reg_base
.globl uart_reg_base
uart_reg_base:  .word 0

.text
.globl main
main:
        jal uartmips_init

$L2:
	# li	$2,-1207828480			# 0xffffffffb8020000
        la $t0, uart_reg_base
        lw $t0, 0($t0)
	lw	$2,0($t0)
	andi	$2,$2,0x200
	srl	$2,$2,9
	beq	$2,$0,$L2
	nop

        la $t0, uart_reg_base
        lw $t0, 0($t0)
	# li	$2,-1207828480			# 0xffffffffb8020000
	li  $3, 'a'
	sw	$3,0($t0)
	#li	$2,-1207828480			# 0xffffffffb8020000



# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall







