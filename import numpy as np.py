import numpy as np
from PIL import Image

a = np.load('output_y.npy')
print(a.shape)
print(a)
b = a.astype('uint8')
c = (a*0.9).astype('uint8')
print(b)
print(c)
img_2 = Image.fromarray(b)
img_2.save('output_y.png', 'png')
