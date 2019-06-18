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
for txt_name in tqdm(txts):
    with open(path + txt_name, 'r') as t:
        cont = t.readlines()
        temp = []
        for lines in cont[:-1]:
            temp.append(lines[:-1].split('\t'))
        filename = txt_name[:-3] + 'csv'
        pd.DataFrame(temp).to_csv(save_path + filename)
        pass
