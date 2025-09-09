.data
input_buf:  .space 12          # buffer to store input string (max 10 digits + \n + \0)
hex_buf:    .space 10          # buffer for printing integer as decimal
newline:    .asciz "\n"

    .text
    .globl main

# Function: read_int
# Reads an integer string from stdin, converts to 32-bit int, stores at address in a0
read_int:
    # a0 = address to store integer

    # --- read input string ---
    li      a7, 63              # syscall: read
    li      a0, 0               # stdin
    la      a1, input_buf
    li      a2, 12              # max 12 bytes
    ecall

    # --- convert ASCII to integer ---
    la      t0, input_buf       # t0 points to input buffer
    li      t1, 0               # t1 = result integer

convert_loop:
    lb      t2, 0(t0)           # load byte
    beq     t2, 10, done_conv   # newline? done
    beq     t2, 0, done_conv    # null terminator? done
    li      t3, 48              # ASCII '0'
    sub     t2, t2, t3          # convert ASCII to number
    li      t3, 10
    mul     t1, t1, t3          # multiply previous result by 10
    add     t1, t1, t2          # add current digit
    addi    t0, t0, 1
    j       convert_loop

done_conv:
    sw      t1, 0(a0)           # store integer in memory

    # --- print integer as decimal using write syscall ---
    # convert integer to string (naive, max 10 digits)
    li      t0, 10              # divisor
    la      t2, hex_buf
    addi    t3, t2, 10          # end pointer
    li      t4, 0               # length counter

    mv      t1, t1              # t1 already has integer
    beqz    t1, store_zero

convert_to_str:
    rem     t5, t1, t0          # t5 = t1 % 10
    addi    t5, t5, 48          # convert to ASCII
    addi    t3, t3, -1
    sb      t5, 0(t3)
    div     t1, t1, t0
    addi    t4, t4, 1
    bnez    t1, convert_to_str
    j       print_number

store_zero:
    addi    t3, t3, -1
    li      t5, 48
    sb      t5, 0(t3)
    li      t4, 1

print_number:
    li      a7, 64              # syscall: write
    li      a0, 1               # stdout
    mv      a1, t3              # buffer start
    mv      a2, t4              # length
    ecall

    # print newline
    li      a7, 64
    li      a0, 1
    la      a1, newline
    li      a2, 1
    ecall

    ret

main:
    la      a0, input_val
    jal     ra, read_int

    # exit
    li      a7, 93              # exit syscall
    li      a0, 0
    ecall