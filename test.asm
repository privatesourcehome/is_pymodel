0 MOVI r1 8
1 MOVI r2 4
2 MOV r3 r1
3 JUMP 11
4 __DEBUG_ASSERT_REG r1 r3 
5 ADD r1 r2
6 __DEBUG_ASSERT_VALUE 12
7 SUB r1 r2
8 __DEBUG_ASSERT_VALUE 4
9 MUL r1 r2
10 __DEBUG_ASSERT_VALUE 32
11 MOVI r3 1
12 MOVI r4 2
13 ADD r3 r4
14 __DEBUG_ASSERT_VALUE 3
15 __DEBUG_EXIT