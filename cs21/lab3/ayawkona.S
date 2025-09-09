.data
prompt:     .asciz "Enter an integer: "
newline:    .asciz "\n"

    .text
    .globl main

read_int:
    addi    sp, sp, -4
    mv      t0, sp

    li      a7, 64
    li      a0, 1
    la      a1, prompt
    li      a2, 17
    ecall

    li      a7, 63
    li      a0, 0
    mv      a1, t0
    li      a2, 4
    ecall

    lw      a0, 0(t0)

    addi    sp, sp, 4
    ret

main:
    jal     ra, read_int

    li      a7, 1
    ecall

    li      a7, 64
    li      a0, 1
    la      a1, newline
    li      a2, 1
    ecall

    li      a7, 93
    li      a0, 0
    ecall