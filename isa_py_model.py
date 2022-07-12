import numpy as np
# numpy is only used for data load&save

# Memory is 128MB both data & instruction
MEM_SIZE = 128000000
comment = ('#','//')
reg = {'r0' : 0, 'r1' : 0, 'r2' : 0, 'r3' : 0, 'r4' : 0, 'r5' : 0, 'r6' : 0,'r7' :  0, 'r8' : 0, 'r9' : 0, 'r10' : 0, 'r11' : 0, 'r12' : 0, 'r13' : 0, 'r14' : 0, 'r15' : 0}
# 코드 길이상 16개만 예시로 들었음.
vreg = {'vr0' : {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0, 13 : 0, 14 : 0, 15 : 0}}
implicit_reg = {'EXIT': False, 'pc': 0, 'cmpreg': 0}

memory  = [np.uint32(0)] * MEM_SIZE
imemory = [np.uint32(0)] * MEM_SIZE

# Memory Load Process
image = np.load('lena_gray.npy')
#for i in range(0, image.shape[0]):
    #memory[i] = image[i]
memory[0] = 169090600
memory[1] = 338181200
memory[2] = 507271800
memory[3] = 676362400
krn = np.load('sobel_x_kernel.npy')
for i in range(0, krn.shape[0]):
    memory[5000000+i] = krn[i]
out = np.load('C:/Users/hooki/Documents/GitHub/is_pymodel/zeros.npy')

for i in range(0, out.shape[0]):
    memory[10000000+i] = out[i]
    
# Memory operation
def LOAD_V(opr):
    for i in range(0, 4):
        vreg[opr[0]][i*4+0] = (memory[reg[opr[1]]+i] & 0xFF000000) >> 24
        vreg[opr[0]][i*4+1] = (memory[reg[opr[1]]+i] & 0xFF0000) >> 16
        vreg[opr[0]][i*4+2] = (memory[reg[opr[1]]+i] & 0xFF00) >> 8
        vreg[opr[0]][i*4+3] = (memory[reg[opr[1]]+i] & 0xFF)
    
    implicit_reg['pc'] = implicit_reg['pc']+1
def LOAD_VS(opr):
    # TODO
    implicit_reg['pc'] = implicit_reg['pc']+1
def LOAD_S(opr):
    reg[opr[0]]=memory[int(opr[1])]
    implicit_reg['pc']=implicit_reg['pc']+1
def STORE_V(opr):
    # TODO
    for i in range(0, 196):
        memory[reg[opr[1]]+i] = np.uint32((np.uint8(vreg[opr[0]][i*4+0]) << 24) + np.uint8(vreg[opr[0]][i*4+1] << 16) + np.uint8(vreg[opr[0]][i*4+2] << 8) + np.uint8(vreg[opr[0]][i*4+3]))
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
    for i in range(0,3):
      vreg[opr[0]][i] = vreg[opr[0]][i]+reg[opr[1]]
    implicit_reg['pc']=implicit_reg['pc']+1
def ADD_SS(opr):
    reg[opr[0]] = reg[opr[1]] + reg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_VV(opr):
    vreg[opr[0]] = vreg[opr[1]] - vreg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_VS(opr):
    for i in range(0,3):
      vreg[opr[0]][i] = vreg[opr[0]][i]-reg[opr[1]]
    implicit_reg['pc']=implicit_reg['pc']+1
def SUB_SS(opr):
    reg[opr[0]] = reg[opr[1]] - reg[opr[2]]
    implicit_reg['pc']=implicit_reg['pc']+1    
def MUL_VV(opr):
    for i in range(0, 3):
          vreg[opr[0]][i] = vreg[opr[1]][i]*vreg[opr[2]][i]
    implicit_reg['pc'] = implicit_reg['pc']+1
def MUL_VS(opr):
    for i in range(0, 3):
      vreg[opr[0]][i] = vreg[opr[0]][i]*reg[opr[1]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def MUL_SS(opr):
    reg[opr[0]] = reg[opr[1]] * reg[opr[2]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def CMP(opr):
    implicit_reg['cmpreg'] = reg[opr[0]] - vreg[opr[1]]
    implicit_reg['pc'] = implicit_reg['pc']+1
def ReLU_V(opr):
    # TODO
    for i in range(0,4):
      vreg[opr][i] = int(vreg[opr][i]*(vreg[opr][i]>0))
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
def __DEBUG_PRTREG(opr):
    print(reg[opr[0]])
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_PRTVREG(opr):
    print(vreg[opr[0]])
    implicit_reg['pc'] = implicit_reg['pc']+1
def __DEBUG_PRT_SUC_MSG(msg):
    print(msg+' test success!')
    return True

# Shutdown
def __DEBUG_EXIT(opr):
    implicit_reg['EXIT'] = True
    implicit_reg['pc'] = implicit_reg['pc']+1

# SYSTEM
def __EXEC_ASM():
    while implicit_reg['EXIT'] == False:
        if int(implicit_reg['pc'])>MEM_SIZE:
            reg['EXIT'] == True
            break
        i = implicit_reg['pc']
        print("current pc : " + str(implicit_reg['pc']))
        #if(implicit_reg['pc'] == 1180425):
            #np.save('./output_lightweight', memory[7000000:7000256])
        op = globals()[imemory[i][0]]
        op(imemory[i][1:])
        pass
def __INIT_IMEM():
    file = open('./new_test.asm', 'r')
    for line in file:
        if line.startswith(comment[:]):
            continue
        instruction = line.split() 
        if instruction:
            imemory[int(instruction[0])] = instruction[1:]

__INIT_IMEM()
__EXEC_ASM()