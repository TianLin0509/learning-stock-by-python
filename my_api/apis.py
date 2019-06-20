import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os
from datetime import timedelta, datetime

data_path_day = 'D:/stock_data/day/'
data_path_minute = 'D:/stock_data/minute/'
ori_data_path = 'D:/new_tdx\T0001\export/'


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
# print(get_data_day('600137', '2019-05-10'))


# ------------------------------------------
#  更新新日期的K线数据
# ------------------------------------------
def trans_csv(txt_name):
    try:
        with open(ori_data_path + txt_name, 'r') as t:
            cont = t.readlines()
            temp = []
            for lines in cont[:-1]:
                temp.append(lines[:-1].split('\t'))
            temp = pd.DataFrame(temp)
            temp = temp.drop(columns=6)  # 去掉成交金额一列，没用
            # 增加涨幅列
            zhangfu = temp.apply(lambda x: format(100 * (float(x[4]) / float(x[1]) - 1), '.2f'), axis=1)
            temp.insert(1, 8, zhangfu)
            # 增加前五日成交量均值，最大值(不包括今日)
            five_means = []
            five_maxs = []
            for i in range(temp.shape[0]):
                select_rows = [x for x in range(i - 5, i) if x >= 0]
                selected = temp.iloc[select_rows][5].apply(lambda y: int(y))
                f_mean = selected.mean() if i > 0 else 0
                f_max = selected.max() if i > 0 else 0
                five_means.append(int(f_mean))
                five_maxs.append(f_max)
            temp.insert(7, 9, five_means)
            temp.insert(8, 10, five_maxs)
            temp.columns = ['date', 'change', 'open', 'high', 'low', 'close', 'amount', 'mean5', 'max5']
            filename = txt_name[:-3] + 'csv'
            pd.DataFrame(temp).to_csv(data_path_day + filename)
    except Exception:
        print(txt_name)


def update_days():
    txts = os.listdir(ori_data_path)
    start_time = time.time()
    with multiprocessing.Pool(8) as p:
        res = list(tqdm(p.imap(trans_csv, txts), total=len(txts)))
    print('总计用时: ', time.time() - start_time)

if __name__ == '__main__':
    update_days()
