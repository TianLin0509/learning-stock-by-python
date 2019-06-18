import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os

# ------------------------------------------
#  比较tushare爬取和本地load的速度差距.快了100倍
# ------------------------------------------

all_stocks = ts.get_stock_basics().index
test_day = '2019-05-09'
path = 'D:/stock_data/day/'


def use_ts():
    start_time = time.time()
    for code in tqdm(all_stocks):
        ts.get_hist_data(code, start=test_day, end=test_day)
    cost_time = time.time() - start_time
    print('共花费%.2f秒' % cost_time)


# 0：日期， 1：开盘 2：最高 3：最低 4：收盘
def local_load():
    csv_paths = os.listdir(path)
    start_time = time.time()
    for csv_path in tqdm(csv_paths):
        content = pd.read_csv(path + csv_path, index_col=0, header=0)
        if content.shape[0] > 0:
            res = content[content['0'] == test_day]
            if res.shape[0] > 0:
                res = res.iloc[0]
    cost_time = time.time() - start_time
    print('共花费%.2f秒' % cost_time)


# use_ts()
local_load()
