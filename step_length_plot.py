import matplotlib.pyplot as plt

L = [197.15298569412528, 248.8342959129288, 230.28185229316077, 187.90963592452573, 207.11801684848206,
     201.8701942022876, 138.4146481808952, 124.94573308510282]
R = [190.1331115452883, 224.8932088766628, 214.71980181567778, 175.9206319879618, 207.11653700147778, 191.5194849406624,
     136.10750150751704, 122.81025231123466]
X = ['NP01', 'NP06', 'NP20', 'NP39', 'PD01', 'PD03', 'PS12', 'PS25']
x = [0, 1, 2, 3, 4, 5, 6, 7]
rects1 = plt.bar(x, height=L, width=0.4, alpha=0.8, color='red', label="L")
rects2 = plt.bar([i + 0.4 for i in x], height=R, width=0.4, alpha=0.8, color='blue', label="R")
plt.ylim(100, 260)

plt.xticks([index + 0.2 for index in x], X)
plt.legend()

plt.savefig('Step_Length.png',dpi=1000)
