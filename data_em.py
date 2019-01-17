import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

data = pd.read_csv('data.csv')
x = data.get('Time')
y = data.get('Pressure')

plt.plot(x,y)
plt.savefig('EM.png',dpi=1000)