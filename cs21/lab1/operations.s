# operations.S
# Checkpoint Task 1

    .text
    .globl _start

_start:
    # 1. Assign some integer to s0 in hexadecimal
    li s0, 0x1A        # example: hex 1A = 26 in decimal

    # 2. Assign some integer to s1 in decimal
    li s1, 25

    # 3. Sum: s2 = s0 + s1
    add s2, s0, s1

    # 4. Difference: s3 = s0 - s1
    sub s3, s0, s1

    # 5. Product: s4 = s0 * s1
    mul s4, s0, s1

    # 6. Quotient: s5 = s0 / s1
    div s5, s0, s1

    # 7. Bitwise AND: s6 = s0 & s1
    and s6, s0, s1

    # 8. Bitwise OR: s7 = s0 | s1
    or s7, s0, s1

    # 9. Bitwise XOR: s8 = s0 ^ s1
    xor s8, s0, s1

    # 10. Bitwise negation of s0: s9 = ~s0
    not s9, s0

    # Exit program (environment call)
    li a7, 93      # exit syscall
    li a0, 0
    ecall
