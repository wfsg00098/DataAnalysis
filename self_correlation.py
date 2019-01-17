import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\" + i):
        if j.split('.')[-1] != "csv":
            continue
        data = pd.read_csv("PressureData\\" + i + "\\" + j)
        # x = data.get('Time').values

        y = data.get('Pressure').values
        x = np.arange(1, len(y), 1)

        y1 = []
        for k in range(len(x)):
            x_mean = sum(x[k:]) / float(len(x[k:]))
            if k != 0:
                y_mean = sum(y[:-k]) / float(len(y[:-k]))
            else:
                y_mean = sum(y) / float(len(y))
            sum1 = 0
            for l in range(0, len(x) - k):
                sum1 += (x[l + k] - x_mean) * (y[l] - y_mean)
            y1.append(sum1)

        y1 = np.divide(y1, y1[0])

        x1 = np.arange(0, len(y1), 1)
        plt.plot(x1, y1)
        plt.savefig("PressureData\\" + i + "\\self-correlation.png", dpi=1000)
        plt.cla()
