import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os
from datetime import *

data_path_day = 'D:/stock_data/day/'
data_path_minute = 'D:/stock_data/minute/'


# ------------------------------------------
#  获取任意股票任意日期的日K信息
# code: 股票代码 day: 日期列表
# ------------------------------------------
def get_data_day(code, day):
    # 输入单天或日期列表都行
    day = day if isinstance(day, list) else [day]
    csv_paths = os.listdir(data_path_day)
    for csv_path in csv_paths:
        if code in csv_path:
            content = pd.read_csv(data_path_day + csv_path, index_col=0, header=0)
            if content.shape[0] > 0:
                res = content[content['date'].isin(day)]
                return res


# ------------------------------------------
#  获取一个包括了一段连续时间的列表
# start_day: 从哪天开始 deltaday: 前连续deltaday天
# ------------------------------------------
def period_days(start_day, deltaday):
    search_days = [(datetime.strptime(start_day, '%Y-%m-%d') - timedelta(days=i)).strftime('%Y-%m-%d') for i in
                   range(deltaday)]
    return search_days


# print(get_data_day('600137', period_days('2019-05-10', 20)))
print(get_data_day('600137', '2019-05-10'))



# ------------------------------------------
#  更新新日期的K线数据
# ------------------------------------------
def update_days():
    