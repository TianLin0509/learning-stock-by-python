import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *

all_stocks = ts.get_stock_basics().index

# ------------------------------------------
#  查找近期强势涨停股（大盘大跌）
# ------------------------------------------
today_day = time.strftime('%Y-%m-%d', time.localtime())
start_day = time.strftime('%Y-%m-%d', time.localtime(time.time() - 365 * 24 * 60 * 60))


def June16(code):
    try:
        temp_result = ts.get_hist_data(code, start=start_day, end=today_day).reset_index()
        # 排除次新股
        if temp_result.iloc[-1].p_change > 12:
            return
        # 筛选近期二板
        zt_index = temp_result[temp_result.p_change > 9.9].index
        erban_index = [x for x in zt_index if (x+1) in zt_index and (x+2) not in zt_index]
        temp = temp_result.iloc[erban_index].set_index('date')
        # 只留下当天大盘不好的
        dapan = [ts.get_hist_data('sh', start=x, end=x).p_change.values[0] for x in temp.index]
        selected = temp.iloc[np.where(np.array(dapan) < -0.9)].copy()
        if len(selected) > 0:
            return code, selected
    except Exception:
        return


if __name__ == '__main__':
    # ------------------------------------------
    #  使用多进程运行target函数
    # ------------------------------------------
    start_time = time.time()
    num = all_stocks.shape[0]
    with multiprocessing.Pool(16) as p:
        res = list(tqdm(p.imap(June16, all_stocks[:num]), total=num))
    print('总计用时: ', time.time() - start_time)
    res = list(filter(None, res))
    csv_res = []
    for i in res:
        i[1].insert(0, 'code', str(i[0]))
        csv_res.append(i[1][['code', 'p_change','volume', 'v_ma10', 'v_ma20']])
    csv_res = pd.concat(csv_res)
    # csv_res.columns = ['代码', '涨幅', '成交量', '10日均成交量', '20日均成交量']
    csv_res.to_csv('June17.csv')
    print(csv_res)
