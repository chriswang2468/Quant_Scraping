import StockSpiderSpe as ss #引入模块
import pandas as pd
import numpy as np
GS = ss.Spider('http://guba.eastmoney.com/list,cjpl,99,f_1.html',1,7418,'财经评论吧')
GS.spider()#第一个数据是帖子信息数据，第二数据是帖子回复数据   
# print("------------------------------------------------")
# print(TZ)