
# Imprime un unico caracter
# Modificado de un ejemplo para mostrar texto hello.s Autor : falcon <wuzhangjin@gmail.com>, 2009/01/17
#
# Compilar con :
#
#	mips-linux-gnu-as -g --gstabs hello_print.s -o hello_print.o
#	mips-linux-gnu-ld -static -o hello_print.elf hello_print.o 


    .data

letra:	.byte	0x41	# Es una 'A' en ASCII

    .text
    .globl main

main:




    li $a0, 1         	# print to standard ouput 
    la $a1, letra    	# La direccion del caracter a imprimir (set the string address)
    li $a2, 1    	# Un solo caracter (set the string length)
    li $v0, 4004      # index of sys_write: 
                      # __NR_write in /usr/include/asm/unistd.h
    syscall           # causes a system call trap.

    # salir
    move $a0, $0      # exit status as 0
    li $v0, 4001      # index of sys_exit
                      # __NR_exit in /usr/include/asm/unistd.h
    syscall

