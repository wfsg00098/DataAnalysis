import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
# import seaborn
import os

def draw(x_data, y_data):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set_title('FFT')
    ax.set_xlabel('Freq')
    ax.set_ylabel('')


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

        yy = fft(y)/len(x)

        y1 = abs(yy)

        x1 = np.arange(len(y))

        yf2 = yy[range(int(len(x) / 1))]
        xf2 = x1[range(int(len(x) / 1))]

        draw(xf2, yf2)
        plt.savefig('fft_normal', dpi=1000)

        break
    break








'''

#采样点选择1400个，因为设置的信号频率分量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，所以这里设置采样频率为1400赫兹（即一秒内有1400个采样点，一样意思的）
x=np.linspace(0,1,1400)

#设置需要采样的信号，频率分量有180，390和600
y=7*np.sin(2*np.pi*180*x) + 2.8*np.sin(2*np.pi*390*x)+5.1*np.sin(2*np.pi*600*x)

yy=fft(y)                     #快速傅里叶变换
yreal = yy.real               # 获取实数部分
yimag = yy.imag               # 获取虚数部分

yf=abs(fft(y))                # 取绝对值
yf1=abs(fft(y))/len(x)           #归一化处理
yf2 = yf1[range(int(len(x)/2))]  #由于对称性，只取一半区间

xf = np.arange(len(y))        # 频率
xf1 = xf
xf2 = xf[range(int(len(x)/2))]  #取一半区间


plt.subplot(221)
plt.plot(x[0:50],y[0:50])
plt.title('Original wave')

plt.subplot(222)
plt.plot(xf,yf,'r')
plt.title('FFT of Mixed wave(two sides frequency range)',fontsize=7,color='#7A378B')  #注意这里的颜色可以查询颜色代码表

plt.subplot(223)
plt.plot(xf1,yf1,'g')
plt.title('FFT of Mixed wave(normalization)',fontsize=9,color='r')

plt.subplot(224)
plt.plot(xf2,yf2,'b')
plt.title('FFT of Mixed wave)',fontsize=10,color='#F08080')


plt.show()
'''