import os
import pandas as pd
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt

for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\"+i):
        if j.split('.')[-1] != "csv":
            continue
        data = pd.read_csv("PressureData\\" + i + "\\" + "data1.csv")
        x = data.get('Time')
        y = data.get('Pressure')

        x = x[300:]
        y = y[300:]

        yy = fft(y) / len(x)

        y1 = abs(yy)

        x1 = np.arange(len(y))

        yf2 = yy[range(int(len(x) / 16))]
        xf2 = x1[range(int(len(x) / 16))]
        plt.plot(xf2, yf2)
        plt.savefig("PressureData\\" + i + "\\" + "fft(16).png", dpi=1000)
        plt.cla()