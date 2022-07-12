import numpy as np
# numpy is only used for data load&save

# Memory is 128MB both data & instruction
MEM_SIZE = 128000000
reg = {'r0' : 0, 'r1' : 0, 'r2' : 0, 'r3' : 0, 'r4' : 0, 'r5' : 0, 'r6' : 0,'r7' :  0, 'r8' : 0, 'r9' : 0, 'r10' : 0, 'r11' : 0, 'r12' : 0, 'r13' : 0, 'r14' : 0, 'r15' : 0}
#vreg will only use 8bit data-types # this is 8*16 = 128b, and will be increased 
vreg = {'vr0' : {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0, 13 : 0, 14 : 0, 15 : 0},
        'vr1' : {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0, 13 : 0, 14 : 0, 15 : 0}, 
        'vr2' : {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0, 13 : 0, 14 : 0, 15 : 0}}
implicit_reg = {'DEBUG_PC_SHOW' : False, 'EXIT': False, 'pc': 0, 'cmpreg': 0}

memory  = [np.uint32(0)] * MEM_SIZE
imemory = [np.uint32(0)] * MEM_SIZE

# Memory Load Process
memory[0] = 169090600 # 10  20  30  40
memory[1] = 338181200 # 20  40  60  80 
memory[2] = 507271800 # 30  60  90  120
memory[3] = 676362400 # 40  80  120 160

# Memory operation
def LOAD_V(opr):
    # TODO Load 는 4bytes 단위로 그냥 load 하고, 계산시에는 두개를 줘야하지 않나? 중간에 type casting되는걸 생각해봐야함. 어차피 Block Diagram에서도 생각해야하는 문제이기 때문.
    for i in range(0, 4): #will be 49
        vreg[opr[0]][i*4+0] = (memory[reg[opr[1]]+i] & 0xFF000000) >> 24
        vreg[opr[0]][i*4+1] = (memory[reg[opr[1]]+i] & 0xFF0000) >> 16
        vreg[opr[0]][i*4+2] = (memory[reg[opr[1]]+i] & 0xFF00) >> 8
        vreg[opr[0]][i*4+3] = (memory[reg[opr[1]]+i] & 0xFF)
    implicit_reg['pc'] = implicit_reg['pc']+1
def LOAD_VS(opr):
    # TODO
    # Stride는 byte 단위로 하니까, 이것은 사용자가 생각할 문제임. 굳이 여기서 어렵게 할 필요가 없음.
    implicit_reg['pc'] = implicit_reg['pc']+1
def LOAD_S(opr):
    reg[opr[0]]=memory[int(opr[1])]
    implicit_reg['pc']=implicit_reg['pc']+1
def STORE_V(opr):
    for i in range(0, 4):  # will be 49
        memory[reg[opr[1]]+i] = (vreg[opr[0]][i*4+0]) * pow(2, 24) + vreg[opr[0]][i*4+1] * pow(2, 16) + vreg[opr[0]][i*4+2] * pow(2, 8) + vreg[opr[0]][i*4+3]
    implicit_reg['pc'] = implicit_reg['pc']+1
def STORE_VS(opr):
    # TODO
    implicit_reg['pc'] = implicit_reg['pc']+1
def STORE_S(opr):
    memory[int(opr[1])][int(opr[2])] = reg[opr[0]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def MOV(opr):
    reg[opr[0]] = int(opr[1])
    implicit_reg['pc'] = implicit_reg['pc']+1

# ALU operation
def ADD_VV(opr):
    vreg[opr[0]] = vreg[opr[1]] + vreg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1
def ADD_VS(opr):
    for i in range(0,15): #will be 196
      vreg[opr[0]][i] = vreg[opr[0]][i]+reg[opr[1]]
    implicit_reg['pc']=implicit_reg['pc']+1
def ADD_SS(opr):
    reg[opr[0]] = reg[opr[1]] + reg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_VV(opr):
    vreg[opr[0]] = vreg[opr[1]] - vreg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_VS(opr):
    for i in range(0, 15):  # will be 196
      vreg[opr[0]][i] = vreg[opr[0]][i]-reg[opr[1]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_SS(opr):
    reg[opr[0]] = reg[opr[1]] - reg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1    
def MUL_VV(opr):
    for i in range(0, 15): # will be 196
          vreg[opr[0]][i] = vreg[opr[1]][i]*vreg[opr[2]][i]
    implicit_reg['pc'] = implicit_reg['pc']+1
def MUL_VS(opr):
    for i in range(0, 15): #will be 196
      vreg[opr[0]][i] = vreg[opr[0]][i]*reg[opr[1]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def MUL_SS(opr):
    reg[opr[0]] = reg[opr[1]] * reg[opr[2]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def CMP(opr):
    implicit_reg['cmpreg'] = reg[opr[0]] - vreg[opr[1]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def RELU_V(opr):
    for i in range(0,15): #will be 196
      vreg[opr[0]][i] = int(vreg[opr[0]][i]*(vreg[opr[0]][i]>0))
    implicit_reg['pc'] = implicit_reg['pc']+1

# Control operation
def JUMP(opr):
    implicit_reg['pc'] = int(opr[0])
def JE(opr):
    if implicit_reg['cmpreg'] == 0:
        implicit_reg['pc'] = int(opr[0])
    else:
        implicit_reg['pc'] = implicit_reg['pc']+1
def JNE(opr):
    if implicit_reg['cmpreg'] != 0:
        implicit_reg['pc'] = int(opr[0])
    else:
        implicit_reg['pc'] = implicit_reg['pc']+1

# Debug function // 그런데, 해저드를 생각하면 DEBUG_PASS를 NOP로 사용하는게 옳지 않을까? -> hazard를 보기
def __DEBUG_PASS(opr):
    implicit_reg['pc'] = implicit_reg['pc']+1  
def __DEBUG_PRT_REG(opr):
    print(reg[opr[0]])
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_PRT_VREG(opr):
    print(vreg[opr[0]])
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_MEM_VIEW(opr):
    for i in range(int(opr[0]), int(opr[1])+1):
        print('memory[' + str(i) + '] : ' + str(memory[i]))
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_PRT_MSG(msg):
    for i in range(0, len(msg)):
        print(msg[i], end=' ')
    print()
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_MEM_2_FILE(opr):
    np.save('./' + opr[2], memory[opr[0]:opr[1]+1])
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_FILE_2_MEM(opr):
    # TODO
    image = np.load(opr[0]+'.npy')
    for i in range(opr[1], image.shape[0]):
        memory[i] = image[i]
    print('File '+str(opr[0]+' is loaded to Memory['+opr[1]+'] to Memory'+opr[2]+']'))
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_EXIT(opr):
    implicit_reg['EXIT'] = True
    implicit_reg['pc'] = implicit_reg['pc']+1

# SYSTEM
def __EXEC_ASM():
    while implicit_reg['EXIT'] == False:
        if implicit_reg['DEBUG_PC_SHOW'] == True:
            print("current pc : " + str(implicit_reg['pc']))
        op = globals()[imemory[implicit_reg['pc']][0]]
        op(imemory[implicit_reg['pc']][1:])
        pass
    
def __INIT_IMEM():
    file = open('./new_test.asm', 'r')
    for line in file:
        if line.startswith('#', '//'):
            continue
        instruction = line.split() 
        if instruction:
            imemory[int(instruction[0])] = instruction[1:]

__INIT_IMEM()
__EXEC_ASM()