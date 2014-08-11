# Hello World en MIPS
#
# assemble: as --gstabs

        .data
        .text
        .global __start

__start:
        li      $t1, 1
        li      $t3, 1
        add     $t0, $t1, $t3

# retorna al SO
        li      $4, 88
        li      $2, 4001
        syscall


