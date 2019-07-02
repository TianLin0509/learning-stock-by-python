import tushare as ts
import requests
import re

# all_stocks = ts.get_stock_basics().index
# print(len(all_stocks))


def get_bankuai(code):
    content = requests.get('http://f10.eastmoney.com/CoreConception/CoreConceptionAjax?code=' + code).text
    index = re.search('"ydnr.*?"},{"zqnm"', content).span()
    res = content[index[0] + 8:index[1] - 10].split(' ')
    with open('done.txt', 'a', encoding='utf-8') as t:
        t.write(code + str(res) + '\n')


ts.set_token('7e025964be399e38c4e2041e76fc6cffb73e0dab7e5efe7b80ab07da')
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code')
total_codes = set([m[0][-2:] + m[0][0:6] for m in data.values])
# get_bankuai(z[0])

with open('done.txt', 'r', encoding='utf-8') as d:
    x = d.readlines()

done_codes = set([m[:8] for m in x])
remained_codes = total_codes - done_codes
print(len(remained_codes))
for i in remained_codes:
    print(i)
    get_bankuai(i)
