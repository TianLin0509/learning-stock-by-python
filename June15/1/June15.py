import tushare as ts
import time

# ------------------------------------------
#  June15. 如何复盘
# ------------------------------------------

today_time = time.strftime('%Y-%m-%d', time.localtime())

# ------------------------------------------
#  找到所有当天涨停股
# ------------------------------------------
today_data = ts.get_today_all()
limitup_stocks = today_data[(today_data.changepercent > 9.9) & (today_data.changepercent < 10.2)]
for code in limitup_stocks.code.values:
    # ticks = ts.get_tick_data(code, date=today_time, src='tt')

    pass
