.text
    .globl main

# Function: read_int
# Reads an integer using ecall 63, stores it in stack, returns it in a0
read_int:
    addi sp, sp, -4        # Reserve 4 bytes on stack
    li a7, 63              # ecall for read integer
    ecall
    sw a0, 0(sp)           # Store input at reserved stack location
    lw a0, 0(sp)           # Load it back into a0 to return
    addi sp, sp, 4         # Restore stack pointer
    ret

# Main function
main:
    call read_int           # Call read_int
    mv t0, a0              # Save the input in t0 if needed

    # Print integer
    li a7, 64               # ecall for print integer
    mv a0, t0
    ecall

    # Exit program
    li a7, 93               # ecall for exit
    li a0, 0                # exit code 0
    ecall