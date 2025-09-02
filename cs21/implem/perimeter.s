main:
    # init a, b, c, d
    addi s0, s0, 6
    addi s1, s1, 7
    addi s2, s2, 6
    addi s3, s3, 1
    #we run perimiter for s0 and s1
    #store result in some register
    #now assign values of s2 to s0 
    #and s3 to s1 before running
    #perimeter again
    jal perimeter
    add s4, zero, a0 # rec1 (we store result of rec1 here)
    
    #we override s0 with s2 and s1 with s3 respective to avoid using excessive registers in the func
    addi s0, s2, 0 
    addi s1, s3, 0
    jal perimeter
    add s5, zero, a0 # rec2
    
    #if else statements to know what to print
    bgt s4, s5, f1
    blt s4, s5, f2
    j done
    
perimeter:
    addi sp, sp, -12 # alloc 3 spaces
    sw t0, 8(sp)
    sw t1, 4(sp)
    sw t2, 0(sp)
    #for the lines above, we just store
    #the values of the temp registers
    #in the stack
    
    
    addi t0, zero, 2 #assign t0 to 2 (so we can mul future num with 2)
    mul t0, t0, s0 #multiply t0 (2) to value of s0 (first number which is the length)
    addi t1, zero, 2 # same proccess as t0
    mul t1, t1, s1 #Kingdom of Nigeria for width
    
    add t2, t0, t1 # (2L + 2W stored in temp reg t2)
    
    add a0, zero, t2 # store perimeter in default return address for funcs a0
    
    jr ra #jump over the border of the usa back to main

f1:
    la a0, str1
    li a7, 4
    ecall
    j done

f2:
    la a0, str2
    li a7, 4
    ecall
    j done
done:
.data
    str1: .asciz "Rec1"
    str2: .asciz "Rec2"
