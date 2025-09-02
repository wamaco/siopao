# indexing.S
# Checkpoint Task 2

    .data
buffer:     .space  30      # buffer for first input (max 10 chars, but allow up to 30 as per a2=30)
digitbuf:   .space  4       # buffer for the index input (1 digit + newline)

    .text
    .globl _start

_start:
    # 1. Read first line into buffer
    li a7, 63           # syscall: read
    li a0, 0            # stdin
    la a1, buffer       # address of buffer
    li a2, 30           # length to read (per problem statement)
    ecall

    # 2. Read digit input into digitbuf
    li a7, 63           # syscall: read
    li a0, 0            # stdin
    la a1, digitbuf
    li a2, 4
    ecall

    # Convert ASCII digit to integer
    lb t0, 0(digitbuf)  # load digit char
    li t1, 48           # ASCII '0'
    sub t0, t0, t1      # t0 = d (as integer)

    # 3. Load character at buffer[d]
    la t2, buffer
    add t2, t2, t0
    lb t3, 0(t2)        # t3 = buffer[d]

    # Print the character
    li a7, 64           # syscall: write
    li a0, 1            # stdout
    mv a1, t2           # address of the character
    li a2, 1            # length 1
    ecall

    # Exit program
    li a7, 93           # exit syscall
    li a0, 0
    ecall
