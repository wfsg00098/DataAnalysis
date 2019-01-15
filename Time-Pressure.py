import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000


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

def draw(x_data,y_data,x_ticklabels):
    _, ax = plt.subplots()
    ax.plot(x_data,y_data)
    ax.set_xticks(x_ticklabels)
    ax.set_xlabel('time')
    ax.set_ylabel('pressure')
    ax.set_title('test')



for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\"+i):
        if j.split('.')[-1] != "txt":
            continue
        data = {}
        raw = None
        with open("PressureData\\"+ i + "\\" + j) as f:
            raw = f.read()
        raw = raw.replace('\r\n','')
        raw = raw.replace('\n', '')
        raw = raw.split(',')

        k = 0
        while k < len(raw) - 1:
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
        xl = x[::(max(x)-min(x))//10]

        with open('1.txt','w') as f:
            f.write(str(x))
            f.write('\n')
            f.write(str(y))
        draw(x,y,xl)
        plt.savefig("PressureData\\"+ i + "\\" + j.split('.')[0] + ".png",dpi = 1000)

        matrix = np.zeros((1080, 480))
        maxm = 0
        k = 0
        while k < len(raw) - 1:
            if int(raw[k+4]) < 30:
                k += 5
                continue
            a, b = get_pixel(int(raw[k+1]), int(raw[k+2]), int(raw[k+3]))
            matrix[a][b] = int(raw[k+4])
            maxm = max(maxm, int(raw[k+4]))
            k += 5
        matrix = np.asarray(matrix,dtype='float64')
        matrix = 255-np.log(1+matrix/maxm*(np.e-1))*255
        img = Image.fromarray(matrix)
        img = img.convert("L")
        img.save("PressureData\\"+ i + "\\" + j.split('.')[0] +".jpg")

        count = 0
        name = i
        for i in x:
            count += 1
            print(count)
            matrix = np.zeros((1080, 480))
            maxm = 0
            k = 0
            while k < len(raw) - 1:
                if int(raw[k + 4]) < 30 or int(raw[k])!= i:
                    k += 5
                    continue
                a, b = get_pixel(int(raw[k + 1]), int(raw[k + 2]), int(raw[k + 3]))
                matrix[a][b] = int(raw[k + 4])
                maxm = max(maxm, int(raw[k + 4]))
                k += 5
            if maxm < 30:
                continue
            matrix = np.asarray(matrix, dtype='float64')
            matrix = 255 - np.log(1 + matrix / maxm * (np.e - 1)) * 255

            img = Image.fromarray(matrix)
            img = img.convert("L")
            img.save("PressureData\\"+ name + "\\"+ str(count) + ".jpg")










