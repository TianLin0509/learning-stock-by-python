import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
from pylab import *

with open('wulianban.txt', 'r') as w:
    a = eval(w.read())
mpl.rcParams['font.sans-serif'] = ['SimHei']
test = a[3]
b = ts.get_hist_data(test[0], end='2019-05-28').reset_index()
c = b.iloc[test[1] - 30: test[1]].sort_index(ascending=False)
d = ts.get_hist_data('sh', end='2019-05-28')
zhishu = []
gujia = c.close.values
for i in c.date.values:
    zhishu.append(d[d.index == i].close)
normalized_zhishu = np.divide(zhishu, np.mean(zhishu) / np.mean(gujia))
d = ts.get_hist_data('sh', end='2019-05-28').reset_index().iloc[test[1] - 30: test[1]].sort_index(ascending=False)
plot(c.date, c.close, marker="^", ms=10, linewidth=2, linestyle="-", color="orange", label='股价走势')
plot(c.date, normalized_zhishu, marker="o", ms=6, linewidth=2, linestyle="-", color="blue", label='大盘走势')
plt.xticks(rotation=50)
plt.ylabel('当日收盘价')
plt.legend(loc='upper right')
plt.savefig("example.png")
plt.show()
