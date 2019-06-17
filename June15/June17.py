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
    start_time = datetime.strptime(row.date, '%Y-%m-%d') - timedelta(days=7)
    end_time = datetime.strptime(row.date, '%Y-%m-%d') + timedelta(days=7)
    res = ts.get_hist_data(row.code, start=start_time.strftime('%Y-%m-%d'),
                           end=end_time.strftime('%Y-%m-%d')).reset_index()
    res.date = res.date.map(lambda x: date2num(datetime.strptime(x, '%Y-%m-%d')))
    pred_for_plot = res.values[:, :5]
    pred_for_plot[:, [3, 4]] = pred_for_plot[:, [4, 3]]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.xaxis_date()
    # fig, ax = plt.subplots()
    candlestick_ochl(ax1, pred_for_plot, colordown='#53c156', colorup='#ff1717', width=0.5)
    plt.xticks(rotation=45)
    plt.title(str(row.code))
    plt.show()
    pass

