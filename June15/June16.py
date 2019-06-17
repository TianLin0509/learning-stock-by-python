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
start_day = time.strftime('%Y-%m-%d', time.localtime(time.time() - 30 * 24 * 60 * 60))


def June16(code):
    try:
        temp_result = ts.get_hist_data(code, start=start_day, end=today_day)
        # 筛选近期涨停个股
        temp = temp_result[(temp_result.p_change > 9.9) & (temp_result.p_change < 11)]
        # 只留下当天大盘不好的
        dapan = [ts.get_hist_data('sh', start=x, end=x).p_change.values[0] for x in temp.index]
        selected = temp.iloc[np.where(np.array(dapan) < -0.6)].copy()
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
    with multiprocessing.Pool(6) as p:
        res = list(tqdm(p.imap(June16, all_stocks[:num]), total=num))
    print("Sub-process(es) done.")
    print(time.time() - start_time)
    res = list(filter(None, res))
    csv_res = []
    for i in res:
        i[1].insert(0, 'code', i[0])
        csv_res.append(i[1][['code', 'p_change','volume', 'v_ma10', 'v_ma20']])
    csv_res = pd.concat(csv_res)
    csv_res.columns = ['代码', '涨幅', '成交量', '10日均成交量', '20日均成交量']
    csv_res.to_csv('June17.csv', encoding='gbk')
    print(csv_res)
