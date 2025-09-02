# msb.S
# Checkpoint Task 3

    .text
    .globl _start

_start:
    # 1. Assign integer to s0 (base 10)
    li s0, 21           # example: 21

    # 2. Compute most significant bit value
    mv t0, s0           # copy input into t0
    li s1, 0            # clear s1

msb_loop:
    beqz t0, done       # if t0 == 0, we’re done
    li t1, 1
    mv s1, t1           # reset s1 to 1
shift_loop:
    srli t0, t0, 1      # shift right by 1
    slli s1, s1, 1      # shift left result by 1
    bnez t0, shift_loop # repeat until t0 becomes 0

done:
    # Now s1 holds MSB value

    # Exit program
    li a7, 93
    li a0, 0
    ecall
