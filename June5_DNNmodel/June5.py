import tushare as ts
import numpy as np
import pandas as pd

ts.set_token('7e025964be399e38c4e2041e76fc6cffb73e0dab7e5efe7b80ab07da')
pro = ts.pro_api()
stocks_sh = pro.stock_basic(exchange='SSE').ts_code
total_data = np.zeros([stocks_sh.size, 5 * 51])
for i, ts_code in enumerate(stocks_sh):
    temp = pro.weekly(ts_code=ts_code, start_date='20180101', end_date='20190101', fields='open,high,low,close,vol')
    temp.vol = temp.vol / temp.vol.mean() * temp.open.mean()
    data = np.reshape(temp.values, -1)
    if data.size == 5 * 51:
        total_data[i] = data
zero_index = np.nonzero(np.mean(total_data, 1) == 0)
np.save('june4.npy', np.delete(total_data, zero_index, 0))
