main:
    jal read_int  
    li a7, 1
    ecall
    li a7, 10    
    ecall          
    
read_int:
    addi sp, sp, -8
    sw ra, 4(sp)
    sw s0, 0(sp)
    
    li a7, 63
    li a0, 0
    la a1, buffer
    li a2, 32
    ecall
    
    la s0, buffer
    li a0, 0
    li t0, 10
    li t2, 48
    li t3, 57
    li t4, 45
    li t5, 1
    
    lb t1, 0(s0)
    bne t1, t4, convert_loop
    li t5, -1
    addi s0, s0, 1
    
convert_loop:
    lb t1, 0(s0)
    beqz t1, convert_done
    blt t1, t2, convert_done
    bgt t1, t3, convert_done
    
    addi t1, t1, -48
    mul a0, a0, t0
    add a0, a0, t1
    
    addi s0, s0, 1
    j convert_loop
    
convert_done:
    mul a0, a0, t5
    lw s0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    jr ra

.data
buffer: .zero 32