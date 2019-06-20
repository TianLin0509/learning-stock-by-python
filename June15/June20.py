import multiprocessing
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import *
import os
from my_utils.utils import *

# ------------------------------------------
#  爬取东财的股票板块信息
# ------------------------------------------

data_path_day = 'D:/stock_data/day/'
codes = [code[:2] + code[3:-4] for code in os.listdir(data_path_day)]
total_info = {}


# for code in tqdm(codes[0:32]):
def get_bankuiinfo(code):
    driver = create_chrome(headless=1)
    try:
        driver.get('http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=' + code)
        result = selenium_wait(driver, '//*[@id="templateDiv"]/div/div[2]/div/p[1]').text
        bankuai_info = result.split(' ')[1:]
        with open('Jun20.txt', 'a') as t:
            t.write(code +  str(bankuai_info) + '\n')
        driver.quit()
    except Exception:
        print(code)
        driver.quit()


if __name__ == '__main__':
    # ------------------------------------------
    #  使用多进程运行target函数
    # ------------------------------------------
    start_time = time.time()
    with open('./Jun20.txt', 'r') as t:
        w = t.readlines()
    done = [x[:8] for x in w]
    codes = list(set(codes).difference(set(done)))
    print(len(codes))
    num = 800
    with multiprocessing.Pool(8) as p:
        res = list(tqdm(p.imap(get_bankuiinfo, codes[:num]), total=num))
    print('总计用时: ', time.time() - start_time)
