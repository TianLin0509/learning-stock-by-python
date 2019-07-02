import pandas as pd

with open('done.txt', encoding='utf-8') as t:
    a = t.readlines()

# 找出所有分类
b = [eval(x[8:]) for x in a]
x = []
for i in b:
    x += i
classes = set(x)
class_dict = {}
for cla in classes:
    class_dict[cla] = []
for i, content in enumerate(b):
    code = a[i][:8]
    for cla in content:
        class_dict[cla].append(code)

with open('class_info.txt', 'w', encoding='utf-8') as t:
    t.write(str(class_dict))
pass