import numpy as np

img = np.zeros(65536).reshape(256, 256)
np.save('./zeros',img)