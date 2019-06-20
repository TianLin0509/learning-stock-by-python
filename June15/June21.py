import requests
import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os
import re

# ------------------------------------------
#  用requests爬取东财的股票板块信息
# ------------------------------------------

data_path_day = 'D:/stock_data/day/'
codes = [code[:2] + code[3:-4] for code in os.listdir(data_path_day)]


def get_bankuai(code):
    content = requests.get('http://f10.eastmoney.com/CoreConception/CoreConceptionAjax?code=' + code).text
    index = re.search('"ydnr.*?"},{"zqnm"', content).span()
    res = content[index[0] + 8:index[1] - 10].split(' ')
    with open('June20.txt', 'a', encoding='utf-8') as t:
        t.write(code + str(res) + '\n')


if __name__ == '__main__':
    # ------------------------------------------
    #  使用多进程运行target函数
    # ------------------------------------------
    start_time = time.time()
    with multiprocessing.Pool(8) as p:
        res = list(tqdm(p.imap(get_bankuai, codes), total=len(codes)))
    print('总计用时: ', time.time() - start_time)



# 下完后有一个乱码的，需要手动去除