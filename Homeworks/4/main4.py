import os

import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

a = sio.loadmat('NP01_1_cut.mat')

matrix = a.get('stepcut')
LR = a.get('LRcheck')[0][0]


def get_pixel(panal, x, y):
    x1 = 0
    y1 = 0
    if panal <= 8:
        x1 = x
        y1 = y + (panal - 1) * 60
    if panal in (9, 10):
        x1 = x + 120
        y1 = y + (panal - 9) * 60
    if panal in (11, 12):
        x1 = x + 120
        y1 = y + (panal - 5) * 60
    if panal in (13, 14):
        x1 = x + 240
        y1 = y + (panal - 13) * 60
    if panal in (15, 16):
        x1 = x + 240
        y1 = y + (panal - 9) * 60
    if panal in range(17, 29):
        x1 = x + 360 + ((panal - 17) // 2) * 120
        y1 = y + 60 - (panal % 2) * 60
    return x1, y1


def check_LR(x, y):
    flag = LR
    k = 0
    for i in range(len(matrix)):
        k = i
        # print(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3],k,x,y)
        if (matrix[i][0] <= x <= matrix[i][1]) and (matrix[i][2] <= y <= matrix[i][3]):
            # print("break")
            break
    if k == len(matrix) - 1:
        # print("no")
        flag = 2
    else:
        if k % 2 == 1:
            if flag == 0:
                flag = 1
            else:
                flag = 0
    return flag


l_data = {}
r_data = {}

for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\" + i):
        raw = None
        with open("PressureData\\" + i + "\\" + j) as f:
            raw = f.read()
        raw = raw.replace('\r\n', '')
        raw = raw.replace('\n', '')
        raw = raw.split(',')

        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 1:
                k += 5
                continue
            if int(raw[k]) in l_data.keys():
                l_data[int(raw[k])] += int(raw[k + 4])
            else:
                l_data[int(raw[k])] = int(raw[k + 4])
            k += 5

        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 0:
                k += 5
                continue
            if int(raw[k]) in r_data.keys():
                r_data[int(raw[k])] += int(raw[k + 4])
            else:
                r_data[int(raw[k])] = int(raw[k + 4])
            k += 5

        MIN = min(min(l_data.keys()), min(r_data.keys()))
        MAX = max(max(l_data.keys()), max(r_data.keys()))

        MAX=1700
        x = []
        y = []
        y1 = []

        for k in range(MIN, MAX + 1):
            if k not in l_data.keys() and k not in r_data.keys():
                continue
            x.append(k)
            temp = 0
            if k in l_data.keys():
                temp = temp + int(l_data[k])
            y.append(temp)
            if k in r_data.keys():
                temp = temp + int(r_data[k])
            y1.append(temp)


        plt.plot(x, y, c='red')
        plt.plot(x, y1, c='blue')
        plt.savefig('组成图.png', dpi=1000)

        break
    break
