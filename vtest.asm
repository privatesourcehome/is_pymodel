0 LOAD_V vr1 adr1
1 LOAD_V vr2 adr2
2 LOAD_V vr3 adr3
# vr1 = [1, 0, 1]
# vr2 = [1, 1, 3]
# vr3 = [1, 0, 1]
3 MUL_VV r1 vr1 vr2
4 __DEBUG_ASSERT_SCALAR_VALUE r1 4
# vr4 = [1*1 + 0*1 + 1*3] -> 4 (dot-product)
5 MUL_VV r2 vr1 vr3
6 __DEBUG_ASSERT_SCALAR_VALUE r2 2
# vr5 = [1*1 + 0*0 + 1*1] -> 2 (dot-product)
7 LOAD_V vr4 adr4
8 LOAD_V vr5 adr5
9 VReLU vr1 vr4
10 __DEBUG_ASSERT_VECTOR_REG vr1 vr5
11 __DEBUG_EXIT