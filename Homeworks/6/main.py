import copy
import random

import pandas as pd
import numpy as np
from fancyimpute import KNN
import statsmodels.formula.api as smf
from sklearn.preprocessing import Imputer

data = pd.read_csv('odata.csv')
ORIGIN_DATA = np.asarray(data, dtype='float64')

data = pd.read_csv('data.csv')
NEW_DATA = np.asarray(data, dtype='float64')

'''
# 去掉原数据5%
for i in range(240):
    x = rd.randint(0, data.shape[0]-1)
    y = rd.randint(1, data.shape[1]-1)
    data[x][y] = -1

with open('data.txt','w')as f:
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            f.write(str(float(data[i][j])))
            if j!= data.shape[1]-1:
                f.write(',')
        f.write('\n')
'''


# 差异度参量, less is better
def judge(data):
    odata = ORIGIN_DATA
    ndata = np.copy(data)
    # min-max标准化
    omax = np.max(odata, axis=0)
    omin = np.min(odata, axis=0)
    nmax = np.max(ndata, axis=0)
    nmin = np.min(ndata, axis=0)
    for i in range(odata.shape[0]):
        for j in range(1, odata.shape[1]):
            odata[i][j] = (odata[i][j] - omin[j]) / (omax[j] - omin[j])
            ndata[i][j] = (ndata[i][j] - nmin[j]) / (nmax[j] - omin[j])

    sum = 0
    for i in range(odata.shape[0]):
        for j in range(1, odata.shape[1]):
            sum += abs(odata[i][j] - ndata[i][j])

    return sum

print('method 0:未进行补全的数据，')
data = np.copy(NEW_DATA)
print("按我们的评判标准出来的差异度是：", judge(data))


print('method 1:缺失值用平均值代替，')
data = np.copy(NEW_DATA)
count, mean = np.zeros(data.shape[1]), np.zeros(data.shape[1])
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            continue
        mean[i] += data[j][i]
        count[i] += 1
count[0] = 1
mean[0] = 1
mean = np.divide(mean, count)

for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = mean[i]

print('按我们的评判标准出来的差异度是：', judge(data))


print('method 2:缺失值用最大值代替，')
data = np.copy(NEW_DATA)
maxm = np.max(data, axis=0)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = maxm[i]
print('按我们的评判标准出来的差异度是：', judge(data))


print('method 3:缺失值用最小值代替，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan
minm = np.nanmin(data, axis=0)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if np.isnan(data[j][i]):
            data[j][i] = minm[i]

print('按我们的评判标准出来的差异度是：', judge(data))



print('method 4:缺失值用众数代替，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan
imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)
imp.fit(data)
data = imp.transform(data)
print('按我们的评判标准出来的差异度是：', judge(data))


print('method 5:缺失值用中位数代替，')
data = np.copy(NEW_DATA)
mid = np.median(data, axis=0)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = mid[i]
print('按我们的评判标准出来的差异度是：', judge(data))



print('method 6:缺失值用knn=3算法生成，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan

data = KNN(k=3).fit_transform(data)
print('按我们的评判标准出来的差异度是：', judge(data))

print('method 7:缺失值用knn=8算法生成，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan

data = KNN(k=8).fit_transform(data)
print('按我们的评判标准出来的差异度是：', judge(data))


print('method 8:缺失值用最小二乘回归法生成，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan

df = pd.DataFrame({'1':data.T[0],'2':data.T[1],'3':data.T[2],'4':data.T[3],'5':data.T[4],'6':data.T[5],'7':data.T[6],'8':data.T[7],'9':data.T[8],'10':data.T[9],'11':data.T[10],'12':data.T[11],'13':data.T[12],'14':data.T[13],'15':data.T[14],'16':data.T[15],'17':data.T[16],'18':data.T[17],'19':data.T[18],'20':data.T[19],'21':data.T[20],'22':data.T[21],'23':data.T[22]})
x = data.T[0]

for i in range(1, data.shape[1]):
    y = data.T[i]
    x1 = []
    y1 = []
    for j in range(len(x)):
        if np.isnan(y[j]):
            continue
        else:
            x1.append(x[j])
            y1.append(y[j])
    est = smf.OLS(y1, x1).fit()
    y2 = est.predict(x)
    for k in range(1, data.shape[1]):
        for j in range(data.shape[0]):
            if np.isnan(data[j][k]):
                data[j][k] = y2[k]

print('按我们的评判标准出来的差异度是：', judge(data))

print('method 9:缺失值用EM算法生成，')
data = np.copy(NEW_DATA)
for i in range(1, data.shape[1]):
    for j in range(data.shape[0]):
        if data[j][i] == -1:
            data[j][i] = np.nan

SIGMA = 6
EPS = 0.0001

# EM算法
def my_EM(X):
    k = 2
    N = len(X)
    Miu = np.random.rand(k, 1)
    Posterior = np.mat(np.zeros((N, 2)))
    dominator = 0
    numerator = 0
    # 先求后验概率
    for iter in range(1000):
        for i in range(N):
            dominator = 0
            for j in range(k):
                dominator = dominator + np.exp(-1.0 / (2.0 * SIGMA ** 2) * (X[i] - Miu[j]) ** 2)
            # print dominator,-1/(2*SIGMA**2) * (X[i] - Miu[j])**2,2*SIGMA**2,(X[i] - Miu[j])**2
            # return
            for j in range(k):
                numerator = np.exp(-1.0 / (2.0 * SIGMA ** 2) * (X[i] - Miu[j]) ** 2)
                Posterior[i, j] = numerator / dominator
        oldMiu = copy.deepcopy(Miu)
        # 最大化
        for j in range(k):
            numerator = 0
            dominator = 0
            for i in range(N):
                numerator = numerator + Posterior[i, j] * X[i]
                dominator = dominator + Posterior[i, j]
            Miu[j] = numerator / dominator
        # print(sum(abs(Miu - oldMiu)))
        if sum(abs(Miu - oldMiu)) < EPS:
            print(Miu, iter)
            break


d1 = data.T[1]
d2 = []
for i in d1:
    if np.isnan(i):
        continue
    d2.append(i)

d2 = [d2]
X = np.asarray(d2,dtype='float64').T
print(X.shape)
my_EM(X)


print('按我们的评判标准出来的差异度是：', judge(data))
