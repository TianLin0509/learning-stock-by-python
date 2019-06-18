import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
from mpl_finance import candlestick_ochl
from pylab import *
from datetime import timedelta, datetime

# ------------------------------------------
#  画出筛选股票的后续走势
# ------------------------------------------

# 防止缺0
csv = pd.read_csv('June17.csv', converters={'code': str})
count = 0
for i in tqdm(range(csv.shape[0])):
    row = csv.iloc[i]
    exact_time = datetime.strptime(row.date, '%Y-%m-%d')
    start_time = exact_time + timedelta(days=1)
    while True:
        res = ts.get_hist_data(row.code, start=start_time.strftime('%Y-%m-%d'),
                               end=start_time.strftime('%Y-%m-%d')).reset_index()
        if res.shape[0] > 0:
            break
        start_time = start_time + timedelta(days=1)
    highest = res.high.values[0]
    lowest = res.low.values[0]
    closed = res.close.values[0]
    ori = ts.get_hist_data(row.code, start=exact_time.strftime('%Y-%m-%d'),
                           end=exact_time.strftime('%Y-%m-%d')).high.values[0]
    zhangfu = (highest - ori) / ori * 100
    diefu = (lowest - ori) / ori * 100
    cl = (closed - ori) / ori * 100
    # print('股票代码： %s 最大涨幅为 %.2f' % (row.code, zhangfu) + '% ' + '最大跌幅为 %.2f' % (diefu))
    # print('股票代码： %s 收盘浮动为 %.2f' % (row.code, cl))
    if cl > 0:
        count += 1

print('收盘上涨概率为 %.2f' % (count / csv.shape[0]))
