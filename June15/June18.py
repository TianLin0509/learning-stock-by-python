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
for i in range(csv.shape[0]):
    row = csv.iloc[i]
    exact_time = datetime.strptime(row.date, '%Y-%m-%d')
    start_time = exact_time + timedelta(days=1)
    end_time = exact_time.strptime(row.date, '%Y-%m-%d') + timedelta(days=7)
    res = ts.get_hist_data(row.code, start=start_time.strftime('%Y-%m-%d'),
                           end=end_time.strftime('%Y-%m-%d')).reset_index()
    highest_day = res.high.values.argmax()
    highest = res.high.values.max()
    ori = ts.get_hist_data(row.code, start=exact_time.strftime('%Y-%m-%d'),
                           end=exact_time.strftime('%Y-%m-%d')).high.values[0]
    zhangfu = (highest - ori) / ori * 100
    print('股票代码： %s 最大涨幅为 %.2f' % (row.code, zhangfu) + '% ' + '在二板后第' + str(highest_day + 1) + '天达到最高')
