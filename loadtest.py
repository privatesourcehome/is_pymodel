import numpy as np

MEM_SIZE = 1000000
vmemory = [0] * MEM_SIZE

img = np.load('lena_gray.npy')
for i in range (0, 3):
    vmemory[i] = img[i]
    print('vmemory['+str(i)+'] : '+str(vmemory[i]))
