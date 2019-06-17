import tushare as ts
import numpy as np
import pandas as pd


ts.set_token('7e025964be399e38c4e2041e76fc6cffb73e0dab7e5efe7b80ab07da')
pro = ts.pro_api()
stocks_sh = pro.stock_basic(exchange='SSE').ts_code