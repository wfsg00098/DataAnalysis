import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

rcParams['figure.figsize'] = 15, 10


def decompose(timeseries):
    # 返回包含三个部分 trend（趋势部分） ， seasonal（季节性部分） 和residual (残留部分)
    decomposition = seasonal_decompose(timeseries)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()

    return trend, seasonal, residual

def test_stationarity(timeseries,name):
    # 这里以一年为一个窗口，每一个时间t的值由它前面12个月（包括自己）的均值代替，标准差同理。

    rolmean = timeseries.rolling(window=12).mean()
    rolstd = timeseries.rolling(window=12).std()

    # plot rolling statistics:
    fig = plt.figure()
    fig.add_subplot()
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='rolling mean')
    std = plt.plot(rolstd, color='black', label='Rolling standard deviation')

    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.savefig(name,dpi=1000)

    # Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    # dftest的输出前一项依次为检测值，p值，滞后数，使用的观测数，各个置信度下的临界值
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical value (%s)' % key] = value

    print(dfoutput)

count = 0

for i in os.listdir("PressureData"):
    for j in os.listdir("PressureData\\"+i):
        if j.split('.')[-1] != "csv":
            continue
        print(count)
        dateparse = lambda dates: pd.to_datetime(dates, format='%Y/%m/%d')
        data = pd.read_csv("PressureData\\" + i + "\\" + 'data1.csv', parse_dates=['Time'], index_col='Time',date_parser=dateparse)
        ts = data['Pressure']
        test_stationarity(ts,"PressureData\\"+i+"\\"+ '判断稳定性.png')
        plt.cla()

        ts_log = np.log(ts)
        ts_log_diff = ts_log - ts_log.shift()
        ts_log_diff.dropna(inplace=True)
        test_stationarity(ts_log_diff,"PressureData\\"+i+"\\"+ '差分.png')
        plt.cla()

        trend, seasonal, residual = decompose(ts_log)
        plt.savefig("PressureData\\"+i+"\\"+ '分解.png',dpi=1000)
        plt.cla()
        residual.dropna(inplace=True)
        test_stationarity(residual,"PressureData\\"+i+"\\"+ '去除趋势和季节性.png')
        plt.cla()

        lag_acf = acf(ts_log_diff, nlags=20)
        lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')
        # Plot ACF:
        plt.subplot(121)
        plt.plot(lag_acf)
        plt.axhline(y=0, linestyle='--', color='gray')
        plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
        plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
        plt.title('Autocorrelation Function')

        # Plot PACF:
        plt.subplot(122)
        plt.plot(lag_pacf)
        plt.axhline(y=0, linestyle='--', color='gray')
        plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
        plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
        plt.title('Partial Autocorrelation Function')
        plt.tight_layout()

        plt.savefig("PressureData\\"+i+"\\"+ 'ACF,PACF图.png',dpi=1000)
        plt.cla()

        orders = (3,1,3)

        #p=7   q=3

        model = ARIMA(ts_log, order=orders)
        results_AR = model.fit(disp=-1)
        plt.figure()
        plt.plot(ts_log_diff)
        plt.plot(results_AR.fittedvalues, color='red')
        plt.title('RSS: %.4f' % sum((results_AR.fittedvalues - ts_log_diff) ** 2))
        plt.savefig("PressureData\\" + i + "\\" + 'ARIMA ('+str(orders) + ').png', dpi=1000)
        plt.cla()

        # ARIMA拟合的其实是一阶差分ts_log_diff，predictions_ARIMA_diff[i]是第i个月与i-1个月的ts_log的差值。
        # 由于差分化有一阶滞后，所以第一个月的数据是空的，
        predictions_ARIMA_diff = pd.Series(results_AR.fittedvalues, copy=True)
        print(predictions_ARIMA_diff.head())
        # 累加现有的diff，得到每个值与第一个月的差分（同log底的情况下）。
        # 即predictions_ARIMA_diff_cumsum[i] 是第i个月与第1个月的ts_log的差值。
        predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
        # 先ts_log_diff => ts_log=>ts_log => ts
        # 先以ts_log的第一个值作为基数，复制给所有值，然后每个时刻的值累加与第一个月对应的差值(这样就解决了，第一个月diff数据为空的问题了)
        # 然后得到了predictions_ARIMA_log => predictions_ARIMA
        predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
        predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
        predictions_ARIMA = np.exp(predictions_ARIMA_log)
        plt.plot(ts)
        plt.plot(predictions_ARIMA)
        plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA - ts) ** 2) / len(ts)))
        plt.savefig("PressureData\\" + i + "\\" + 'ARIMA 预测.png', dpi=1000)
        plt.cla()
        count += 1

        break
    break