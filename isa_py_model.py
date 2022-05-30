import numpy as np

MEM_SIZE=10000000
comment = ('#','//') 
reg = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0,
       'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0, 'r12': 0, 'r13': 0, 'r14': 0, 'r15': 0, 'r16': 0, 'r17': 0, 'r18': 0}
spreg = {'result': 0,'pc': 0, 'EXIT': False, 'EQ': False}
vreg = {'vr1':0, 'vr2':0, 'vr3':0, 'vr4':0, 'vr5':0}
addr = {'adr1': 0, 'adr2': 1, 'adr3': 2, 'adr4': 3, 'adr5': 4}
memory  = [0] * MEM_SIZE
vmemory = [0] * MEM_SIZE
kmemory = [0] * MEM_SIZE
img = np.load('lena_gray.npy')
for i in range(0, img.shape[0]):
    vmemory[i] = img[i]
krn = np.load('sobel_x_kernel.npy')
for i in range(0, krn.shape[0]):
    memory[5000000+i] = krn[i]
out = np.load('zeros.npy')
for i in range(0, out.shape[0]):
    memory[7000000+i] = out[i]

# Memory operation
def LOAD_V(opr):
    vreg[opr[0]] = vmemory[opr[1]]
    reg['pc'] = reg['pc']+1
    '''
def LOAD_V(opr):
    vreg[opr[0]] = vmemory[addr[opr[1]]]
    reg['pc'] = reg['pc']+1
    '''
def LOAD_S(opr):
    reg[opr[0]]=memory[reg[opr[1]]]
    reg['pc']=reg['pc']+1
def LOAD_SI(opr):
    reg[opr[0]]=int(opr[1])
    reg['pc']=reg['pc']+1

'''
def STORE_S(opr):
    memory[int(opr[1])]=reg[opr[0]]
    reg['pc']=reg['pc']+1
'''
def STORE_S(opr):
    memory[opr[1]][opr[2]] = vreg[opr[0]]
    reg['pc'] = reg['pc']+1
def STORE_V(opr):
    vmemory[reg[opr[1]]]=vreg[opr[0]]
    reg['pc']=reg['pc']+1
def MOV_VS(opr):
    # vreg 지정, 몇번째 데이터, to reg
    reg[opr[0]] = vmemory[opr[1]][opr[2]]
    reg['pc'] = reg['pc']+1
    
# Control operation
def JUMP(opr):
    reg['pc']=int(opr[0])
def JNE(opr):
    if reg['EQ'] == False:
        reg['pc'] = int(opr[0])
    else: reg['pc'] = reg['pc']+1
def JE(opr):
    if reg['EQ'] == True:
        reg['pc'] = int(opr[0])
    else: reg['pc'] = reg['pc']+1
def BE(opr):
    if reg['EQ'] == True:
        reg['pc'] = reg['pc'] + int(opr[0])
    else: reg['pc'] = reg['pc']+1
def BNE(opr):
    if reg['EQ'] == False:
        reg['pc'] = reg['pc'] + int(opr[0])
    else: reg['pc'] = reg['pc']+1
    
# ALU operation
def ADD_VV(opr):
    vreg[opr[0]] = vreg[opr[1]] + vreg[opr[2]]
    reg['pc']=reg['pc']+1
def ADD_VS(opr):
    vreg[opr[0]] = vreg[opr[1]] + reg[opr[2]]
    reg['pc']=reg['pc']+1
def SUB_VV(opr):
    vreg[opr[0]] = vreg[opr[1]] - vreg[opr[2]]
    reg['pc']=reg['pc']+1
def SUB_VS(opr):
    vreg[opr[0]] = vreg[opr[1]] - reg[opr[2]]
    reg['pc']=reg['pc']+1
def MUL_VV(opr):
    reg[opr[0]] = np.dot(vreg[opr[1]], np.transpose(vreg[opr[2]]))
    reg['pc'] = reg['pc']+1
def MUL_VS(opr):
    vreg[opr[0]] = vreg[opr[1]] * vreg[opr[2]]
    reg['pc'] = reg['pc']+1
def CMP(opr):
    reg['result'] = reg[opr[0]]-reg[opr[1]]
    if(reg['result']==0):
        reg['EQ']=True
    else: reg['EQ']=False
    reg['pc'] = reg['pc']+1
def VReLU(opr):
    vreg[opr[0]] = vreg[opr[1]]*(vreg[opr[1]]>0)
    reg['pc'] = reg['pc']+1

# Debug function
def __DEBUG_ASSERT_SCALAR_VALUE(opr):
    assert reg[opr[0]] == int(opr[1]) and __DEBUG_PRT_SUC_MSG(
        msg='__DEBUG_ASSERT_VALUE Test Success'), 'fail'
    reg['pc'] = reg['pc']+1
def __DEBUG_ASSERT_SCALAR_REG(opr):
    assert reg[opr[0]] == reg[opr[1]] and __DEBUG_PRT_SUC_MSG(
        msg='__DEBUG_ASSERT_REG Test Success'), 'fail'
    reg['pc'] = reg['pc']+1
def __DEBUG_ASSERT_VECTOR_REG(opr):
    assert np.array_equal(vreg[opr[0]], vreg[opr[1]]) and __DEBUG_PRT_SUC_MSG(
        msg='__DEBUG_ASSERT_VALUE Test Success'), 'fail'
    reg['pc'] = reg['pc']+1
def __DEBUG_PRTREG(opr):
    print(reg[opr[0]])
    reg['pc'] = reg['pc']+1
def __DEBUG_EXIT(opr):
    reg['EXIT'] = True
    reg['pc'] = reg['pc']+1
def __DEBUG_PRT_SUC_MSG(msg='success!'):
    print(msg)
    return True
 
#Unused function
def ADD_SS(opr):
    reg[opr[0]] = reg[opr[1]] + reg[opr[2]]
    reg['pc']=reg['pc']+1
def SUB_SS(opr):
    reg[opr[0]] = reg[opr[1]] - reg[opr[2]]
    reg['pc'] = reg['pc']+1
def MUL_SS(opr):
    reg[opr[0]] = reg[opr[1]] * reg[opr[2]]
    reg['pc'] = reg['pc']+1
 
# SYSTEM
def __EXEC_ASM():
    while reg['EXIT'] == False:
        if int(reg['pc'])>MEM_SIZE:
            reg['EXIT'] == True
            break
        i = reg['pc']
        print("current pc : " + str(reg['pc']))
        op = globals()[memory[i][0]]
        op(memory[i][1:])
        pass
def __INIT_IMEM():
    file = open('./vtest.asm', 'r')
    for line in file:
        if line.startswith(comment[:]):
            continue
        instruction = line.split() 
        if instruction:
            memory[int(instruction[0])] = instruction[1:]

__INIT_IMEM()
__EXEC_ASM()
