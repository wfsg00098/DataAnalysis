import os
import scipy.io as sio
import math
import numpy as np

def get_center(a,b,x,y):
    return (a+b)/2,(x+y)/2

L = []
R = []


for k in os.listdir("PressureData"):
        a = sio.loadmat("PressureData\\" + k + "\\cut.mat")
        matrix = a.get('stepcut')
        LR = a.get('LRcheck')[0][0]

        left = []
        right = []

        for i in range(2, len(matrix)):
            x1, y1 = get_center(matrix[i - 2][0], matrix[i - 2][1], matrix[i - 2][2], matrix[i - 2][3])
            x2, y2 = get_center(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3])
            d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            if i % 2 == 0:
                left.append(d)
            else:
                right.append(d)

        if LR == 1:
            left, right = right, left

        L.append(np.mean(left))
        R.append(np.mean(right))

print(L)
print(R)