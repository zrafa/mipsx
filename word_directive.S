	.data
contador:
	.word	0x12345678

	.text
	.globl main
main:
	li $v0, 10 # código llamada al sistema para exit
	syscall
