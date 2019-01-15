import os

import scipy.io as sio
from matplotlib import pyplot as plt

Reverse = 0
a = None
matrix = None
LR = None


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
    if k == len(matrix):
        # print("no")
        flag = 2
    else:
        if k % 2 == 1:
            if flag == 0:
                flag = 1
            else:
                flag = 0
    return flag


def check_FB(x, y):
    global Reverse
    k = 0
    for i in range(len(matrix)):
        k = i
        # print(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3],k,x,y)
        if (matrix[i][0] <= x <= matrix[i][1]) and (matrix[i][2] <= y <= matrix[i][3]):
            # print("break")
            break
    if k == len(matrix):
        # print("no")
        return 2

    if abs(matrix[k][1] - matrix[k][0]) >= abs(matrix[k][3] - matrix[k][2]):
        d = 2  # 竖着
    else:
        d = 1  # 横着

    if d == 1:
        Reverse = 1
        if y >= ((matrix[k][2] + matrix[k][3]) // 2):
            flag = 1  # 前
        else:
            flag = 0  # 后
    else:
        if x <= ((matrix[k][0] + matrix[k][1]) // 2):
            flag = 1  # 前
        else:
            flag = 0  # 后
        if Reverse == 1:
            if flag == 1:
                flag = 0
            else:
                flag = 1
    return flag


for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\" + i):
        if j.split('.')[-1] != "txt":
            continue

        raw = None
        with open("PressureData\\" + i + "\\" + j) as f:
            raw = f.read()
        raw = raw.replace('\r\n', '')
        raw = raw.replace('\n', '')
        raw = raw.split(',')

        a = sio.loadmat("PressureData\\" + i + "\\cut.mat")
        matrix = a.get('stepcut')
        LR = a.get('LRcheck')[0][0]

        Reverse = 0
        data = {}
        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 0:
                k += 5
                continue
            if check_FB(a, b) != 1:
                k += 5
                continue
            if raw[k] in data.keys():
                data[raw[k]] += int(raw[k + 4])
            else:
                data[raw[k]] = int(raw[k + 4])
            k += 5
        x1 = []
        y1 = []
        for k in data.keys():
            if int(data[k]) < 100:
                continue
            x1.append(int(k))
            y1.append(int(data[k]))
        LF, = plt.plot(x1, y1, c='blue', label='LF')

        Reverse = 0
        data = {}
        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 0:
                k += 5
                continue
            if check_FB(a, b) != 0:
                k += 5
                continue
            if raw[k] in data.keys():
                data[raw[k]] += int(raw[k + 4])
            else:
                data[raw[k]] = int(raw[k + 4])
            k += 5
        x2 = []
        y2 = []
        for k in data.keys():
            if int(data[k]) < 100:
                continue
            x2.append(int(k))
            y2.append(int(data[k]))
        LB, = plt.plot(x2, y2, c='green', label='LB')

        Reverse = 0
        data = {}
        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 1:
                k += 5
                continue
            if check_FB(a, b) != 1:
                k += 5
                continue
            if raw[k] in data.keys():
                data[raw[k]] += int(raw[k + 4])
            else:
                data[raw[k]] = int(raw[k + 4])
            k += 5
        x3 = []
        y3 = []
        for k in data.keys():
            if int(data[k]) < 100:
                continue
            x3.append(int(k))
            y3.append(int(data[k]))
        RF, = plt.plot(x3, y3, c='red', label='RF')

        Reverse = 0
        data = {}
        k = 0
        while k < len(raw) - 1:
            a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
            if check_LR(a, b) != 1:
                k += 5
                continue
            if check_FB(a, b) != 0:
                k += 5
                continue
            if raw[k] in data.keys():
                data[raw[k]] += int(raw[k + 4])
            else:
                data[raw[k]] = int(raw[k + 4])
            k += 5
        x4 = []
        y4 = []
        for k in data.keys():
            if int(data[k]) < 100:
                continue
            x4.append(int(k))
            y4.append(int(data[k]))
        RB, = plt.plot(x4, y4, c='yellow', label='RB')
        plt.legend(handles=[LF, LB, RF, RB])
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_LRFB.png", dpi=1000)
        plt.cla()

        LF, = plt.plot(x1, y1, c='blue', label='LF')
        LB, = plt.plot(x2, y2, c='green', label='LB')
        plt.legend(handles=[LF, LB])
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_L_FB.png", dpi=1000)
        plt.cla()

        RF, = plt.plot(x3, y3, c='red', label='RF')
        RB, = plt.plot(x4, y4, c='yellow', label='RB')
        plt.legend(handles=[RF, RB])
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_R_FB.png", dpi=1000)
        plt.cla()

        LF, = plt.plot(x1, y1, c='blue', label='LF')
        RF, = plt.plot(x3, y3, c='red', label='RF')
        plt.legend(handles=[LF, RF])
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_LR_F.png", dpi=1000)
        plt.cla()

        LB, = plt.plot(x2, y2, c='green', label='LB')
        RB, = plt.plot(x4, y4, c='yellow', label='RB')
        plt.legend(handles=[LB, RB])
        plt.savefig("PressureData\\" + i + "\\" + j.split('.')[0] + "_LR_B.png", dpi=1000)
        plt.cla()
