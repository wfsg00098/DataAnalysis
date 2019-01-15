import os

import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt

a = sio.loadmat('NP01_1_cut.mat')

matrix = a.get('stepcut')
LR = a.get('LRcheck')[0][0]
print(matrix[0][3])