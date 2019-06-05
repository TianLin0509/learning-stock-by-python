# learning-stock-by-python
股市亏空太多。。决定使用python，花里胡哨分析一通，看似炒股，实则学习嘿嘿。

# requirement
* tushare  **获取股票信息** [安装方法](http://tushare.org/index.html#id5)

# 相关
* 通过这个库，学习一下pandas等知名python库的使用
* 也希望得到一些之前所不熟知的股市暗藏规律
* 如果能赚点零花钱再好不过了(先把亏的钱补上再说)
* 顺便记录一下每天的股海历程，公众号 **PythonicStock**，欢迎关注。。

# 已经完成的一些代码：
* [统计中小板股票涨停后次日上涨的概率](https://github.com/TianLin0509/learning-stock-by-python/blob/master/May28.py)
* [利用多进程统计所有股票两连后第三日开盘价高于第二日概率](https://github.com/TianLin0509/learning-stock-by-python/blob/master/May29_2.py)
* 准备验证fyy的回测模型,考虑近期科研略忙，分步完成吧..:
  - [收集所有五连板股票并写入txt文件](https://github.com/TianLin0509/learning-stock-by-python/blob/master/June1_fyy_model/June1.py)
  - [结合matplotlib,画出五连板股票的后续走势，寻找抄底契机](https://github.com/TianLin0509/learning-stock-by-python/blob/master/June1_fyy_model/June2.py)
  - <img src="https://github.com/TianLin0509/learning-stock-by-python/blob/master/June1_fyy_model/example.png" width = "350" height = "300" alt="五连板后走势图" align=center />
  - [使用fyy回测模型，找到上车点（分为June3和June3_2, 前者负责找出合适股票，后者负责画图）](https://github.com/TianLin0509/learning-stock-by-python/tree/master/June1_fyy_model)
  - <img src="https://github.com/TianLin0509/learning-stock-by-python/blob/master/June1_fyy_model/002288.png" width = "350" height = "300" alt="fyy回测模型图" align=center /> 
* [收集上证股票2018年周线图及成交量，并以numpy矩阵形式保存以供神经网络训练](
https://github.com/TianLin0509/learning-stock-by-python/blob/master/June5_DNNmodel/June4.py)
* [通过神经网络预测周线图](https://github.com/TianLin0509/learning-stock-by-python/blob/master/June5_DNNmodel/June4.py).具体的思路见文件夹下readme..可以视作反面教材，不过吹响了DNN的号角.
  - <img src="https://github.com/TianLin0509/learning-stock-by-python/blob/master/June5_DNNmodel/example.png" width = "350" height = "300" alt="神经网络预测周线" align=center /> 
