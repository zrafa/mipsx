
                .data
.global uart_reg_base
.globl uart_reg_base
uart_reg_base:  .word 0

	.file	1 "serial.c"
	.section .mdebug.abi32
	.previous
	.abicalls
	.text
	.align	2
	.set	nomips16
	.set	nomicromips
	.ent	AthrUartPut
	.type	AthrUartPut, @function
AthrUartPut:
	.frame	$fp,24,$31		# vars= 8, regs= 1/0, args= 0, gp= 8
	.mask	0x40000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	addiu	$sp,$sp,-24
	sw	$fp,20($sp)
	move	$fp,$sp
	move	$2,$4
	sb	$2,24($fp)
$L2:
	# li	$2,-1207828480			# 0xffffffffb8020000
        la $t0, uart_reg_base
	lw	$2,0($t0)
	sw	$2,8($fp)
	lw	$2,8($fp)
	andi	$2,$2,0x200
	srl	$2,$2,9
	beq	$2,$0,$L2
	nop

	lb	$2,24($fp)
	andi	$2,$2,0xff
	sw	$2,8($fp)
	lw	$2,8($fp)
	ori	$2,$2,0x200
	sw	$2,8($fp)
	li	$2,-1207828480			# 0xffffffffb8020000
	lw	$3,8($fp)
	sw	$3,0($2)
	#li	$2,-1207828480			# 0xffffffffb8020000
        la $t0, uart_reg_base
	lw	$2,0($t0)
	nop
	move	$sp,$fp
	lw	$fp,20($sp)
	addiu	$sp,$sp,24
	j	$31
	nop

	.set	macro
	.set	reorder
	.end	AthrUartPut
	.size	AthrUartPut, .-AthrUartPut
	.align	2
	.globl	serial_putc
	.set	nomips16
	.set	nomicromips
	.ent	serial_putc
	.type	serial_putc, @function
serial_putc:
	.frame	$fp,32,$31		# vars= 0, regs= 2/0, args= 16, gp= 8
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	addiu	$sp,$sp,-32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	move	$2,$4
	sb	$2,32($fp)
	lb	$2,32($fp)
	move	$4,$2
	.option	pic0
	jal	AthrUartPut
	nop

	.option	pic2
	nop
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addiu	$sp,$sp,32
	j	$31
	nop

	.set	macro
	.set	reorder
	.end	serial_putc
	.size	serial_putc, .-serial_putc
	.align	2
	.globl	main
	.set	nomips16
	.set	nomicromips
	.ent	main
	.type	main, @function
main:
        jal uartmips_init
	.frame	$fp,32,$31		# vars= 0, regs= 2/0, args= 16, gp= 8
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro

	addiu	$sp,$sp,-32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	li	$4,97			# 0x61
	.option	pic0
	jal	serial_putc
	nop

	.option	pic2
	nop
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addiu	$sp,$sp,32
	j	$31
	nop

	.set	macro
	.set	reorder
	.end	main
	.size	main, .-main
	.ident	"GCC: (Debian 5.3.1-8) 5.3.1 20160205"
