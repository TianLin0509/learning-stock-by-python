# =====================================
#  统计中小板涨停后股票第二天上涨的概率
# =====================================

import tushare as ts

sz50 = ts.get_sme_classified()
total_zhangting = 0
total_diertianzhang = 0

for i in range(sz50.shape[0]):
    gupiao_code = sz50.code[i]
    print(str(i) + ':股票代码为:', gupiao_code)
    print(50 * '=')
    a = ts.get_hist_data(gupiao_code, end='2019-05-26').reset_index()
    # print(a)
    b = a[a.p_change > 9.8]
    c = b.index
    d = a.iloc[c - 1]
    e = d[d.p_change > 0]
    total_zhangting += d.shape[0]
    total_diertianzhang += e.shape[0]
    try:
        print('涨停后第二天涨的概率为：', e.shape[0] / d.shape[0])
    except ZeroDivisionError:
        print('这傻逼股从未涨停过')
    print(50 * '=')

print(50 * '-')
print('在中小板 ' + str(sz50.shape[0]) + ' 只股票近三年总共产生了 ' + str(total_zhangting) + ' 次涨停')
print('其中有 ' + str(total_diertianzhang) + ' 次第二天股票上涨了')
print('上涨概率为: ', str(total_diertianzhang / total_zhangting))
