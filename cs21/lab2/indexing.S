# Lab 2 Checkpoint 2
# 202315337

.text

main:
    # === Step 1: read first line of input (string) ===
    li a7, 63          # syscall 63 = read
    li a0, 0           # file descriptor 0 = stdin
    la a1, str         # buffer to store the input string
    li a2, 30          # max number of bytes to read
    ecall              # perform read, result stored in 'str'
    
    # === Step 2: read second line of input (digit index) ===
    li a7, 63          # syscall 63 = read
    li a0, 0           # stdin
    la a1, dig         # buffer to store the digit
    li a2, 10          # max number of bytes to read
    ecall
    
    # === Step 3: convert ASCII digit → integer ===
    la t0, dig         # load address of digit buffer
    lb t1, 0(t0)       # load first byte (ASCII code of digit)
    addi t1, t1, -48   # convert ASCII code to int (e.g. '3' → 3)
    
    # === Step 4: get character from str at index d ===
    la t2, str         # base address of the string
    add t2, t2, t1     # add index offset to base (str + d)
    lb t3, 0(t2)       # load the character at that address
    
    # === Step 5: print the selected character ===
    la t4, print       # load address of print buffer
    sb t3, 0(t4)       # store the character into print buffer
    li a7, 64          # syscall 64 = write
    li a0, 1           # file descriptor 1 = stdout
    la a1, print       # address of character to print
    li a2, 1           # print only 1 byte
    ecall              # perform write

.data

print: .byte 0         # 1-byte buffer for output
str: .zero 30          # buffer for string input (30 bytes max read)
dig: .zero 5           # buffer for digit input
