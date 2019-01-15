import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000


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


def draw(x_data, y_data):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set_title('test')
    ax.set_xlabel('lag')
    ax.set_ylabel('Normalized autocorrelation')


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
            if int(raw[k]) in data.keys():

                data[int(raw[k])] += int(raw[k + 4])
            else:
                data[int(raw[k])] = int(raw[k + 4])
            k += 5

        x = []
        y = []
        for k in range(min(data.keys()), max(data.keys()) + 1):
            x.append(k)
            if k in data.keys():
                y.append(data[k])
            else:
                y.append(0)

        for k in range(1, len(y) - 1):
            if y[k] == 0:
                y[k] = (y[k - 1] + y[k + 1]) // 2

        x = x[300:]
        y = y[300:]


        y1 = []
        for k in range(len(x)):
            x_mean = sum(x[k:]) / float(len(x[k:]))
            if k != 0:
                y_mean = sum(y[:-k]) / float(len(y[:-k]))
            else:
                y_mean = sum(y) / float(len(y))
            sum1 = 0
            for l in range(0, len(x)-k):
                sum1 += (x[l+k] - x_mean) * (y[l] - y_mean)
            y1.append(sum1)

        y1 = np.divide(y1,y1[0])

        x1 = []
        for k in range(1,1449):
            x1.append(k)

        draw(x1,y1)
        plt.savefig('相关.png',dpi=1000)

        break
    break
