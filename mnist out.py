import matplotlib.pylab as plt
from dataset.mnist import load_mnist
import pickle
import numpy as np
import sys
import os
sys.path.append("./dataset")  # 이때, dataset 폴더는 실행하는 py 파일의 경로와 일치해야 한다.

(train_image_data, train_label_data), (test_image_data,
                                       test_label_data) = load_mnist(flatten=True, normalize=False)


def mnist_show(n):
    image = train_image_data[n]
    image_reshaped = image.reshape(28, 28)
    image_reshaped.shape
    label = train_label_data[n]
    plt.figure(figsize=(4, 4))
    plt.title("sample of " + str(label))
    plt.imshow(image_reshaped, cmap="gray")
    plt.show()
    image_reshape_out = np.zeros(np.uint32(196))
    for i in range(0,196):
        temp = np.uint32(0)
        temp = np.uint32(image[i*4+0] << 24)+np.uint32((image[i*4+1] << 16)) + np.uint32((image[i*4+2] << 8)) + np.uint32((image[i*4+3]))
        image_reshape_out[i] = temp
    np.save('./mnist_4_image', image_reshape_out)
    image_reshape_out_restore = np.zeros(784)
    for i in range(0, 196):
        a1 = (np.uint32(image_reshape_out[i]) & 0xFF000000) >> 24
        a2 = (np.uint32(image_reshape_out[i]) & 0x00FF0000) >> 16
        a3 = (np.uint32(image_reshape_out[i]) & 0x0000FF00) >> 8
        a4 = (np.uint32(image_reshape_out[i]) & 0x000000FF)
        image_reshape_out_restore[i*4+0] = a1
        image_reshape_out_restore[i*4+1] = a2
        image_reshape_out_restore[i*4+2] = a3
        image_reshape_out_restore[i*4+3] = a4
    plt.imshow(image_reshape_out_restore.reshape(28,28), cmap="gray")
    plt.show()
        
            
    
mnist_show(4)