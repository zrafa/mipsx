
# File: hello.s -- Say Hello to MIPS Assembly Language Programmer
# Author: falcon <wuzhangjin@gmail.com>, 2009/01/17


    .data
memoria:
stradr: .asciiz "hello, world!\n"
strlen: .word . - stradr  # current address - the string address
# end

    .text
    .globl main

main:

                      # print sth. via sys_write
    li $a0, 1         # print to standard ouput 
    la $a1, stradr    # set the string address
    lw $a2, strlen    # set the string length
    li $v0, 4004      # index of sys_write: 
                      # __NR_write in /usr/include/asm/unistd.h
    syscall           # causes a system call trap.

                      # exit via sys_exit
    move $a0, $0      # exit status as 0
    li $v0, 4001      # index of sys_exit
                      # __NR_exit in /usr/include/asm/unistd.h
    syscall




