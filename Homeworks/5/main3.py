import numpy as np
import matplotlib.pyplot as plt
import sys


def distancematrix(test):
    leng = len(test)
    resmat = np.zeros([leng, leng], np.float32)
    for i in range(leng):
        for j in range(leng):
            resmat[i, j] = np.linalg.norm(test[i] - test[j])
    return resmat  # 返回距离矩阵


def mds(test, deg):
    length = len(test)
    re = np.zeros((length, length), np.float32)
    if (deg > length):
        deg = length
    D = distancematrix(test)
    ss = 1.0 / length ** 2 * np.sum(D ** 2)
    for i in range(length):
        for j in range(length):
            re[i, j] = -0.5 * (D[i, j] ** 2 - 1.0 / length * np.dot(D[i, :], D[i, :]) - 1.0 / length * np.dot(D[:, j],
                                                                                                              D[:,
                                                                                                              j]) + ss)

    A, V = np.linalg.eig(re)
    list_idx = np.argpartition(A, deg - 1)[-deg:]
    a = np.diag(np.maximum(A[list_idx], 0.0))
    return np.matmul(V[:, list_idx], np.sqrt(a))


# 使用 Dijkstra 算法获取最短路径，并更新距离矩阵
# test: 距离矩阵，大小 m * m
# start：最短路径的起始点，范围 0 到 m-1
def usedijk(test, start):
    count = len(test)
    col = test[start].copy()
    rem = count - 1
    while rem > 0:
        i = np.argpartition(col, 1)[1]
        length = test[start][i]
        for j in range(count):
            if test[start][j] > length + test[i][j]:
                test[start][j] = length + test[i][j]
                test[j][start] = test[start][j]
        rem -= 1
        col[i] = float('inf')


# isomap 算法的具体实现
# test：需要降维的矩阵
# target：目标维度
# k：k 近邻算法中的超参数
# return：降维后的矩阵
def isomap(test, target, k):
    inf = float('inf')
    count = len(test)
    if k >= count:
        raise ValueError('K is too large')
    mat_distance = distancematrix(test)
    knear = np.ones([count, count], np.float32) * inf
    for idx in range(count):
        topk = np.argpartition(mat_distance[idx], k)[:k + 1]
        knear[idx][topk] = mat_distance[idx][topk]
    for idx in range(count):
        usedijk(knear, idx)
    return mds(knear, target)


if __name__ == '__main__':
    print('开始降维.....')

    x = [120, 122.5, 117.25, 150, 149, 141.5, 105, 111.25, 112, 112.75, 120, 113.75, 117, 118, 107.75, 115, 127.25,
         128.5, 156, 154, 118, 112.5, 111.75, 102.5, 107.5, 118.75, 134, 124, 112.5, 115.5, 111.25, 133, 125.5, 120,
         124.5, 129, 142, 137.5, 106.25, 94.75, 103.5, 116, 119.75, 124.75, 111.75, 128.25, 146.5, 141.5, 122, 116.5,
         136.75, 135.5, 140.5, 135, 136.5, 138.75, 140.25, 158.5, 118.5, 111.75, 117, 113, 121, 136.5, 132.5, 143, 146,
         156, 154.5, 167, 125, 125.75, 139.75, 130.5, 98.75, 144.5, 130.25, 174, 123.75, 54.7, 168.5, 117.75, 132,
         118.25, 122.25, 79.5, 101.5, 113.25, 113, 125.25, 102.5, 102.75, 110.25, 118.5, 119, 133, 125.75, 131.75,
         129.75, 125.5, 122.5, 122, 112.75, 119.25, 124.75, 128.75, 128.75, 123.75, 135, 96, 99.25, 104, 118.75, 114.25,
         120, 125, 118, 130.5, 138, 135.5, 108.25, 106.75, 106, 135, 149, 129, 117.25, 115, 148, 139, 131.5, 113.75,
         110, 114.5, 113.5, 121, 123.5, 122, 93.25, 95.67, 94.25, 118.5, 127.5, 133, 105.75, 101.5, 96.75, 114.5, 116,
         104.5, 109.5, 67.17, 112.5, 105.25, 109.25, 125.5, 123.75, 118.75, 98.5, 94.75, 101, 102.5, 100.25, 151.5, 154,
         147, 146, 142.5, 105, 109.25, 120.5, 121, 112.75, 112.25, 115, 106.25, 116.25, 122.5, 121.5, 122.75, 102.75,
         111.75, 108.75, 106.25, 104.5, 103.25, 97.25, 102.5, 101.5, 99.5, 104.5, 105.5, 110.5, 111.25, 114, 124.5, 118,
         124, 116.5, 98, 93, 113.5, 107, 111.75, 108.5, 99.75, 101.5, 91.75, 88.75, 96, 105.75, 105, 119.5, 122, 120.5,
         109, 108.75, 112]
    y = [121, 125, 117.5, 148.5, 150, 137, 106, 114, 113, 115.5, 121.5, 115, 119.5, 118.5, 104.25, 116, 129, 131.5,
         155.5, 148, 121, 113.5, 112, 99.25, 108, 119.5, 138.5, 131.5, 112, 115.5, 112.25, 131, 124, 122, 125.5, 128.5,
         144, 142.5, 105.25, 99.75, 104.5, 119, 125.5, 129, 116.5, 132, 147.5, 143.5, 124.5, 119, 143, 137, 140.5,
         136.5, 133.5, 144.5, 149, 164, 121.5, 111, 123, 112.5, 122, 129.5, 133.5, 140, 143.5, 154, 152, 158.5, 126.5,
         126.5, 144.5, 130, 103, 144.5, 136.5, 159.5, 123, 54.38, 163.5, 119.5, 129, 122, 126, 78.5, 99.75, 113.5, 114,
         124.5, 102, 105.5, 108.25, 122, 113.5, 134.5, 127, 139, 141, 126, 124.5, 126.5, 108.75, 119, 126.5, 127, 127.5,
         125, 135, 95.25, 99, 101.25, 117.5, 114.5, 121, 124.5, 116, 128.5, 133, 128, 106.5, 111, 106.5, 135, 146.5,
         132.5, 118, 119.5, 150, 132.5, 127, 113.5, 110, 121, 113, 117, 123.5, 124.5, 92.5, 98.5, 93.5, 119.5, 130.5,
         131.5, 104.5, 102.5, 96, 116.5, 117, 103.5, 112, 72.33, 113.5, 108.25, 110.5, 128, 125, 123, 96.5, 94, 102,
         102, 100, 164, 155.5, 143.5, 140.5, 139.5, 108.25, 112.5, 124.5, 123.5, 116, 114, 117.5, 109, 119.5, 123.5,
         121.5, 123.5, 100.5, 110, 107, 107.75, 107, 103.25, 99.5, 104, 104.5, 98, 102.25, 106.5, 113, 113.5, 115,
         129.5, 126, 132, 115, 100.5, 94.75, 113.5, 113.5, 111.5, 108, 104, 101.75, 92.5, 88.25, 100.5, 105.75, 104,
         123, 125, 117, 108, 104.5, 112]

    x = np.asarray(x, dtype='float64')
    y = np.asarray(y, dtype='float64')

    D = np.zeros((218, 218), dtype='float64')

    for i in range(218):
        for j in range(218):
            D[i][j] = int(np.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2))

    outcome = isomap(D, 2, 217)
    sys.stdout.write('降维完成\n')
    plt.plot(np.resize(outcome.T[0],218),np.resize(outcome.T[1],218),'bx')
    plt.show()


