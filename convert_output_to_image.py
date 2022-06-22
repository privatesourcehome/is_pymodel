import numpy as np
from PIL import Image

a = np.load('output_sobel_test.npy')
b = a.astype('uint8')
img_2 = Image.fromarray(b)
img_2.save('output_sobel_test.png', 'png')
