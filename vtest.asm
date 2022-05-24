0 LOAD_V vr1 adr1
1 LOAD_V vr2 adr2
2 LOAD_V vr3 adr3
3 MUL_VV vr4 vr1 vr2
4 __DEBUG_ASSERT_VALUE 4
5 MUL_VV vr5 vr1 vr3
6 __DEBUG_ASSERT_VALUE 2
# vr1 = [1, 0, 1]
# vr2 = [1, 1, 3]
# vr3 = [1, 0, 1]
# vr4 = [1*1 + 0*1 + 1*3] -> 4 (dot-product)
# vr5 = [1*1 + 0*0 + 1*1] -> 2 (dot-product)
7 __DEBUG_EXIT