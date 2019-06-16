import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from functools import wraps
from tqdm import tqdm
import os

all_stocks = ts.get_stock_basics().index


# ------------------------------------------
#  将函数包装为多进程
# ------------------------------------------
def multi_proc_deco(func):
    @wraps(func)
    def multiprocess_func(queue, *args, **kwargs):
        results = func(*args)
        # print(zhangting_days)
        queue.put(results)

    return multiprocess_func


# ------------------------------------------
#  查找所有涨停股
# ------------------------------------------
@multi_proc_deco
def zhangting_chazhao(codes, start='2019-04-01'):
    zhangting_days = []
    for code in codes:
        result = ts.get_hist_data(code, start=start, end='2019-05-28')
        zhangting_days.append(result[result.p_change > 9.9])
    return zhangting_days
    # print(zhangting_days)


# ------------------------------------------
#  查找近期强势涨停股（大盘大跌）
# ------------------------------------------
today_time = time.strftime('%Y-%m-%d', time.localtime())
start_time = time.strftime('%Y-%m-%d', time.localtime(time.time() - 30 * 24 * 60 * 60))


@multi_proc_deco
def June16(codes):
    #print(multiprocessing.current_process().name)
    results = []
    if multiprocessing.current_process().name == 'Process-1':
        codes = tqdm(codes)
    for code in codes:
        # print(code)
        try:
            temp_result = ts.get_hist_data(code, start=start_time, end=today_time)
            results.append(temp_result[temp_result.p_change > 9.9])
        except Exception:
            pass
    return results


if __name__ == '__main__':
    # ------------------------------------------
    #  使用多进程运行target函数
    # ------------------------------------------
    queue = multiprocessing.Queue()
    p_pool = []
    multi_process = 8
    step = all_stocks.shape[0] // multi_process
    time_start = time.time()
    for i in range(multi_process):
        st = step * i
        if i == multi_process - 1:
            ed = all_stocks.shape[0]
        else:
            ed = st + step
        codes = all_stocks[st: ed]
        p = multiprocessing.Process(target=June16, args=(queue, codes))
        p.start()
        p_pool.append(p)
    for p in p_pool:
        p.join()

    temp = []

    # ------------------------------------------
    #   提取多进程输出
    # ------------------------------------------

    for i in range(multi_process):
        temp += queue.get()

    print(len(temp))
