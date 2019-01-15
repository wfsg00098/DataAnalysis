import os

import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt

a = sio.loadmat('PS13_1_cut.mat')

matrix = a.get('stepcut')
LR = a.get('LRcheck')[0][0]


def draw(x_data, y_data, x_ticklabels):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set_xticks(x_ticklabels)
    ax.set_xlabel('time')
    ax.set_ylabel('pressure')
    ax.set_title('test')


def get_pixel(panal,x,y):
    x1 = 0
    y1 = 0
    if panal <= 8:
        x1 = x
        y1 = y + (panal-1) * 60
    if panal in (9,10):
        x1 = x + 120
        y1 = y + (panal-9) * 60
    if panal in (11,12):
        x1 = x + 120
        y1 = y + (panal-5) * 60
    if panal in (13,14):
        x1 = x + 240
        y1 = y + (panal-13) * 60
    if panal in (15,16):
        x1 = x + 240
        y1 = y + (panal-9) * 60
    if panal in range(17,29):
        x1 = x + 360 + ((panal-17) // 2 ) * 120
        y1 = y + 60 - (panal % 2) * 60
    return x1,y1



def check_LR(x, y):
    flag = LR
    k = 0
    for i in range(len(matrix)):
        k = i
        # print(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3],k,x,y)
        if (matrix[i][0] <= x <= matrix[i][1]) and (matrix[i][2] <= y <= matrix[i][3]):

            # print("break")
            break
    if k == len(matrix)-1:
        # print("no")
        flag = 2
    else:
        if k%2 == 1 :
            if flag == 0:
                flag = 1
            else:
                flag = 0
    return flag



for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\" + i):
        data = {}
        raw = None
        with open("PressureData\\" + i + "\\" + j) as f:
            raw = f.read()
        raw = raw.replace('\r\n', '')
        raw = raw.replace('\n', '')
        raw = raw.split(',')

        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a,b) != 0:
                k+=5
                continue
            if raw[k] in data.keys():
                data[raw[k]] += int(raw[k + 4])
            else:
                data[raw[k]] = int(raw[k + 4])
            k += 5
        x = []
        y = []
        for k in data.keys():
            if int(data[k]) < 100:
                continue
            x.append(int(k))
            y.append(int(data[k]))

        xl = x[::(max(x) - min(x)) // 10]
        draw(x, y, xl)
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_L.png", dpi=1000)


        break
    break


