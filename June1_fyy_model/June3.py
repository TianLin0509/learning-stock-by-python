import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

with open('wulianban.txt', 'r') as w:
    a = eval(w.read())

finds = []
for test in a:
    # print(test[0])
    b = ts.get_hist_data(test[0], end='2019-05-28').reset_index()
    c = b.iloc[test[1] - 30: test[1]].sort_index(ascending=False)
    downs_x = c[c.p_change < 0][['date', 'p_change']]
    try:
        index0 = downs_x.index[0]
        # 放缓下跌那天
        fanghuanri = downs_x[downs_x.p_change > -3].index[0]
        # 大跌时段
        dadieshiduan = c.loc[index0:fanghuanri+1]
        # print(dadieshiduan)
        if dadieshiduan.size > 1 and dadieshiduan.size == dadieshiduan[dadieshiduan.p_change < -5].size:
            e = c.loc[fanghuanri - 1:fanghuanri - 5]
            f = e[e.p_change < -5]
            if f.size > 0:
                d = ts.get_hist_data('sh', end='2019-05-28')
                g = d[d.index == f.iloc[0].date]
                if g.p_change.values[0] < -1:
                    print('find!')
                    finds.append((test[0], test[1], f.iloc[0].date))
    except IndexError:
        continue

with open('find.txt', 'w') as f:
    f.write(str(finds))
