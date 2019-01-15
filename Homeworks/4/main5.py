
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import parallel_coordinates



plt.rcParams['savefig.dpi'] = 1000
plt.rcParams['figure.dpi'] = 1000

data = pd.read_csv('a.csv')
data_1 = data[["gender","age","weight","length","step_distance_left","step_range_left","step_speed_left","step_freq_left","standtime_left","shaketime_left","shakepre_left","step_distance_right","step_range_right","step_speed_right","step_freq_right","standtime_right","shaketime_right","shakepre_right","period","standtime","corner1_time","corner2_time"]]

parallel_coordinates(data_1, "gender")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=21, fancybox=True, shadow=True)
plt.savefig('parallel figure.png',dpi=1000)
'''

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import parallel_coordinates

data = pd.read_csv('iris.csv')
data_1 = data[['Species', 'Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width']]

parallel_coordinates(data_1, 'Species')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fancybox=True, shadow=True)
plt.show()
'''