# ====================================================
#  统计所有A股三年内涨停后第第三天开盘价高于第二天概率
# ====================================================
import multiprocessing
import time
import tushare as ts

# 获得所有股票代码
all_stocks = ts.get_stock_basics().index
print('共有 ' + str(all_stocks.shape[0]) + ' 只股票')

# g代表第三天高于第二天的情况数
# f代表涨停总数
def t(start, ed, queue):
    gt = 0
    ft = 0
    for i in range(start, ed):
        gupiao_code = all_stocks[i]
        print(str(i) + ':股票代码为:', gupiao_code)
        print(50 * '=')
        try:
            a = ts.get_hist_data(gupiao_code, end='2019-05-26').reset_index()
            # print(a)
            b = a[a.p_change > 9.8]
            # 涨停的日子
            c = b.index
            # 涨停第二天和第三天
            d = a.iloc[c - 1].reset_index()
            e = a.iloc[c - 2].reset_index()
            f = e.open - d.open
            g = f[f > 0]
            gt += g.shape[0]
            ft += f.shape[0]
            # print(g.shape[0], f.shape[0])
        except AttributeError:
            print('该股票近三年没有记录！')
    queue.put((gt, ft))


# 使用多线程加快运行速度
if __name__ == '__main__':
    queue = multiprocessing.Queue()
    p_pool = []
    multi_process = 10
    step = all_stocks.shape[0] // multi_process
    time_start = time.time()
    for i in range(multi_process):
        st = step * i
        if i == multi_process - 1:
            ed = all_stocks.shape[0]
        else:
            ed = st + step
        p = multiprocessing.Process(target=t, args=(st, ed, queue))
        p.start()
        p_pool.append(p)
    for p in p_pool:
        p.join()

    G = 0
    F = 0
    for i in range(multi_process):
        gt, ft = queue.get()
        G += gt
        F += ft
    print('近三年所有A股共有 '+ str(F) +' 次涨停发生')
    print('其中第三天开盘高于第二天的有 ' + str(G) + ' 次，概率为 ' + str(G/F))
    time_end = time.time()
    print('总共用时为： ', str(time_end - time_start) + ' 秒')
