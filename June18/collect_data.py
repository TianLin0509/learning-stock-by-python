import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os

# ------------------------------------------
#  将通达信导出数据转换为CSV格式

# ------------------------------------------
path = 'D:/new_tdx\T0002\export/'
save_path = 'D:/stock_data/day/'
all_stocks = ts.get_stock_basics().index
txts = os.listdir(path)


# ts.get_today_all()
# for txt_name in tqdm(txts):
def trans_csv(txt_name):
    try:
        with open(path + txt_name, 'r') as t:
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
            pd.DataFrame(temp).to_csv(save_path + filename)
    except Exception:
        print(txt_name)


if __name__ == '__main__':
    # ------------------------------------------
    #  使用多进程运行target函数
    # ------------------------------------------
    start_time = time.time()
    with multiprocessing.Pool(8) as p:
        res = list(tqdm(p.imap(trans_csv, txts), total=len(txts)))
    print('总计用时: ', time.time() - start_time)
    res = list(filter(None, res))