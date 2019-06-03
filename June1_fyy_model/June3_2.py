import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

with open('find.txt', 'r') as f:
    a = eval(f.read())

mpl.rcParams['font.sans-serif'] = ['SimHei']
for test in a:
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
    plt.xticks(rotation=60)
    plt.scatter(test[2], c[c.date == test[2]].close, color='', marker='o', edgecolors='r', s=200, label='fyy推荐上车点')
    plt.ylabel('当日收盘价')
    plt.legend(loc='upper right')
    plt.title('股票代码：' + test[0])
    plt.savefig('./figs/' + test[0] + '.png')
    plt.show()
    pass
