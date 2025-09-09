# Lab 2 Item 3.1 
# 202315337

.text

main:
    # initialize the variables p & h
    li s0, 10 # p pigs
    li s1, 3  # h holes
    li s4, 1  # const. for assertions
    
    # assertion: check if p >= 1 and h >= 1
    blt s0, s4, bc_fail
    blt s1, s4, bc_fail
    
    # if p and h pass assertions, proceed
    div s2, s0, s1 # s2 = p // h; max pigs per hole
    rem s3, s0, s1 # s3 = p % h; leftover pigs
    
    j done
    
bc_fail:
    la a0, bc_fail_str
    li a7, 4
    ecall
    
done:
    li a7, 10
    ecall
    
.data

bc_fail_str: .string "Assumptions were not met!"