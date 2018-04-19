import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import requests

f = lambda x: x.text.strip()#去除空字符串

class Spider():

    def __init__(self,url,start,stop,name):
        self.url = url		
        self.start = start
        self.stop = stop
        self.name = name
    
    def time_re(self,str):
        return(re.findall('\d+[-]\d+[-]\d+\s{2}\d+[:]\d+[:]\d+',str.text)[0])
	
    def test(self):
        print(self.url)

    def spider(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
        TZ_data = pd.DataFrame()
        HT_data = pd.DataFrame()
        i = self.start
        print('<div class="articleh" id="ad_topic"></div>');
        while i <= self.stop: #设定抓取页数
            next = ',f_'+str(i)+'.html'#按照发帖时间排序
            href = self.url.replace(',f_1.html',next)#股吧帖子列表页面
            print(href);
            resp=requests.get(href,headers=headers) #获取股吧页面
            html = BeautifulSoup(resp.text,'lxml') #股吧页面解析
            Title= html.find_all(class_="articleh")

            for item in Title:
                if str(item)=='<div class="articleh" id="ad_topic"></div>':
                    continue
                if item.find_all('em')==[] or item.find_all('em')[0].text=='':
                    info = item.find_all('span',class_='l3')[0].find_all('a')[0]#每个帖子的具体信息
                    LL= int(item.find_all('span',class_="l1")[0].contents[0])#判断帖子是否异常的指标
                    if LL > 50 :
                        hrefT = 'http://guba.eastmoney.com'+ info['href'] #帖子链接
                        respT=requests.get(hrefT,headers=headers) #获取帖子信息
                        htmlT = BeautifulSoup(respT.text,'lxml') #帖子首页页面解析
                        fttime_html= htmlT.find_all(class_="zwfbtime")
                        fttime = re.findall('\d+[-]\d+[-]\d+\s\d+[:]\d+[:]\d+',fttime_html[0].contents[0])[0]#发帖时间
                        
                        biaoti_text = htmlT.find_all(id="zwconttbt")[0].text#发帖标题
                        biaoti_text = biaoti_text.strip()#去除空字符串
                        biaoti_info = htmlT.find_all(class_="stockcodec")[0].text#标题详细内容     未去除空字符串
                        biaoti_info = biaoti_info.strip()#去除空字符串
                        # print(biaoti_info)
                        biaoti = {'time':[fttime],'tiezi':[biaoti_info]}
                        data = pd.DataFrame(biaoti,columns=['time','tiezi'])#帖子的标题发帖时间信息，每次更新
                        tiezi_info = htmlT.find_all(text=re.compile('var num=\d+;var count=\d+'))#根据标签内容查找
                        ll,xg = re.findall('\d+',tiezi_info[0])
                        pinglun = htmlT.find_all(text=re.compile('var pinglun_num=\d+'))
                        pinglun= re.findall('var pinglun_num=\d+',pinglun[0])
                        pl = re.findall('\d+',pinglun[0])[0]
                        
                        tiezi = {'date':fttime,'title':biaoti_text,'num_visited':ll,'num_comment':pl,'related_arc':xg,'url':hrefT,'contents':biaoti_info}
                        # print(tiezi)
                        print(biaoti_text)
                        tiezi_data = pd.DataFrame(tiezi,index=['0']) #每次都更新
                        HT_data_sub = pd.DataFrame()
                        j = 1
                        # print(biaoti_text)
                        ply = np.ceil(int(pl)/30)
                        while j <= ply:  #抓取全部评论
                            nextT = '_'+str(j)+'.html'
                            hrefTJ = hrefT.replace('.html',nextT)#帖子页面
                            respT = requests.get(hrefTJ,headers=headers) #获取帖子页面
                            htmlT = BeautifulSoup(respT.text,'lxml') #帖子页面解析
                            huitie_time = htmlT.find_all('div',class_="zwlitime")[0].text
                            temp=huitie_time.split(" ")
                            huitie_time=temp[1]+" "+temp[-1]  
                            huitie_info = htmlT.find_all('div',class_="zwlitext stockcodec")[0].text.strip()
                            userid=htmlT.find_all('span',class_="zwnick")[0].find_all('a')[0]["data-popper"]
                            username=htmlT.find_all('span',class_="zwnick")[0].find_all('a')[0].text
                            print(huitie_time)
                            print(huitie_info)
                            j += 1
            print('第%s页抓取完毕！'%i)
            i += 1
        print('爬取完毕,共爬取%s第%s页到第%s页帖子数据' %(self.name,self.start,self.stop))
        return(TZ_data,HT_data)


    if __name__ == '__main__':
        print('请输入爬取网址及爬取页数!') 