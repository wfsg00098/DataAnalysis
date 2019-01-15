import os

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\" + i):
        if j.split('.')[-1] != "csv":
            continue
        data = pd.read_csv("PressureData\\" + i + "\\" + j)
        time = data.get('Time')
        pressure = data.get('Pressure')
        single = data.get('single')
        double = data.get('double')
        triple = data.get('triple')
        move = data.get('move')

        A, = plt.plot(time, pressure, c='red', label='pressure')
        E, = plt.plot(time, move, c='blue', label='move_mean3')
        B, = plt.plot(time, single, c='yellow', label='single0.7')
        C, = plt.plot(time, double, c='green', label='double0.7')
        D, = plt.plot(time, triple, c='purple', label='triple0.7')
        plt.legend(handles=[A, E, B, C, D])
        plt.savefig("PressureData\\" + i + "\\all.png", dpi=1000)
        plt.cla()

        A, = plt.plot(time, pressure, c='red', label='pressure')
        B, = plt.plot(time, single, c='yellow', label='single0.7')
        C, = plt.plot(time, double, c='green', label='double0.7')
        D, = plt.plot(time, triple, c='purple', label='triple0.7')
        plt.legend(handles=[A, B, C, D])
        plt.savefig("PressureData\\" + i + "\\all_smoothing.png", dpi=1000)
        plt.cla()

        A, = plt.plot(time, pressure, c='red', label='pressure')
        B, = plt.plot(time, single, c='yellow', label='single0.7')
        plt.legend(handles=[A, B])
        plt.savefig("PressureData\\" + i + "\\single.png", dpi=1000)
        plt.cla()

        A, = plt.plot(time, pressure, c='red', label='pressure')
        C, = plt.plot(time, double, c='green', label='double0.7')
        plt.legend(handles=[A, C])
        plt.savefig("PressureData\\" + i + "\\double.png", dpi=1000)
        plt.cla()

        A, = plt.plot(time, pressure, c='red', label='pressure')
        D, = plt.plot(time, triple, c='purple', label='triple0.7')
        plt.legend(handles=[A, D])
        plt.savefig("PressureData\\" + i + "\\triple.png", dpi=1000)
        plt.cla()

        A, = plt.plot(time, pressure, c='red', label='pressure')
        E, = plt.plot(time, move, c='blue', label='move_mean3')
        plt.legend(handles=[A, E])
        plt.savefig("PressureData\\" + i + "\\move.png", dpi=1000)
        plt.cla()