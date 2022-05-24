0 MOVI r4 5
1 MOVI r1 0
# comment
// comment
2 MOVI r2 1
3 CMP r4 r1
4 JNE 6
5 JE 9
6 ADD r1 r2
7 MOV r1 result
8 JUMP 3
9 __DEBUG_ASSERT_REG r1 r4
10 __DEBUG_EXIT