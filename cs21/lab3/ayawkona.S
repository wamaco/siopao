# cs21le3a.s
# RISC-V program to read an integer using ecall 63, store it on the stack, and print it

.text
main:
    # Save ra to stack
    addi sp, sp, -8        # Allocate stack space
    sd ra, 0(sp)           # Save return address

    # Call read_int
    jal ra, read_int       # Call read_int, result in a0

    # Print the integer (ecall 1)
    mv a1, a0              # Move result to a1 for printing
    li a0, 1               # ecall 1: print integer
    ecall

    # Print newline
    li a0, 11              # ecall 11: print character
    li a1, '\n'            # Load newline character
    ecall

    # Exit program (ecall 93)
    li a0, 93              # ecall 93: exit
    li a1, 0               # Exit code 0
    ecall

    # Restore ra and return
    ld ra, 0(sp)           # Restore return address
    addi sp, sp, 8         # Deallocate stack space
    ret

read_int:
    # Allocate stack space for the integer (4 bytes)
    addi sp, sp, -8        # Allocate 8 bytes (ensure alignment)
    mv t0, sp              # Save stack pointer to t0

    # Prepare buffer for ecall 63
    mv a0, t0              # a0 = address to store input (stack)
    li a1, 4               # a1 = max bytes to read (4 bytes for 32-bit int)
    li a2, 0               # a2 = file descriptor 0 (stdin)
    li a7, 63              # ecall 63: read
    ecall

    # Load the integer from stack
    lw a0, 0(sp)           # Load 32-bit integer into a0

    # Deallocate stack space
    addi sp, sp, 8         # Restore stack pointer

    ret