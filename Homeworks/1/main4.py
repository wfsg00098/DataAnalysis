import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

data = [665,635,655,490,520,505,716.67,695,655,630,575,655,670,645,590,580,480,485,580,655,530,463.33,440,380,385,646.67,605,650,515,515,540,635,610,515,530,696.67,760,680,600,595,535,670,693.33,700,560,590,535,770,680,595,620,700,720,670,645,665,670,670,635,585,475,575,525,460,635,615,635,590,550,560,730,765,555,916.67,583.33,625,610,525,565,1290,580,570,630,490,500,503.33,645,680,590,730,892,540,865,595,485,470,670,605,610,690,805,700,613.33,543.33,533.33,573.33,545,540,590,615,590,580,575,500,670,660,715,600,580,610,763.33,725,890,715,615,625,700,680,665,650,655,680,685,680,670,675,700,665,850,786.67,790,660,595,605,595,665,665,665,646.67,635,540,585,580,756.67,740,850,840,835,790,1587.5,790,720,710,660,720,690,650,810,750,735,600,620,760,740,735,865,730,700,700,685,686.67,700,685,670,666.67,700,626.67,575,575,693.33,620,645,580,595,610,530,525,505,625,655,680,550,535,545,776.67,896.67,903.33,733.33,720,760,893.33,726.67,630,620,645,730,770,740]

data.sort()

y = {}
for i in range(len(data)):
    if data[i] in y.keys():
        y[data[i]] += 1
    else:
        y[data[i]] = 1

temp = []
for i in y.keys():
    temp.append(y[i])


for i in range(1,len(temp)):
    temp[i] += temp[i-1]

_, ax = plt.subplots()
ax.set_ylabel('Stand Time')
ax.set_xlabel('QQ')
ax.set_title('Stand Time QQ-Plot')

ax.plot(temp,np.unique(data))
plt.show()