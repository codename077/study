#requests+selenium爬取12306，缺少错误输入检测，后期预计会加入购票环节
import requests
import re
import datetime
from urllib.request import urlopen, quote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
z=u'([\u4e00-\u9fa5]+)\|([A-Z]+)\|([a-z]+)'
url='https://kyfw.12306.cn'
xx='/otn/resources/js/framework/station_name.js?station_version=1.9201'
response=requests.get(url+xx)
response.encoding='utf-8'
html=response.text
print(html)
r=re.findall(z,html)
print(r)
def shuru(qidian,zhongdian):
    cz=0
    for i in range(len(r)):
        if qidian==r[i][0]:
            c=list(r[i])
        if zhongdian==r[i][0]:
            m=list(r[i])
    return c,m
ss=input("输入出发城市：")
cc=input("输入目标城市：")
q,m=shuru(ss,cc)
#print('查询到的车票网址信息：')
tomorrow=datetime.date.today()+datetime.timedelta(days=1)
lianjie='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},{}&ts={},{}&date={}&flag=N,N,Y'.format(quote(q[0]),q[1],quote(m[0]),m[1],str(tomorrow))
#print(q,m,str(today))
print('查询到的车票网址信息：',lianjie)
browser=webdriver.Edge(executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe")
browser.get(lianjie)
browser.maximize_window()
browser.find_element_by_id('qd_closeDefaultWarningWindowDialog_id').click()
zxx=browser.find_element_by_id('queryLeftTable').text
bt=browser.find_element_by_id('float').text
c1=re.split('\n|\s+',bt)
c2=re.split('\n|\s+',zxx)
for i in range(len(c1)):
    if c1[i] in ['商务座', '二等座', '高级', '软卧', '硬卧']:
        c1[i]=c1[i]+'\n'+c1[i+1]
        c1.pop(i+1)
    if i==len(c1)-2:
        break
xx0=[]
c2.remove('复')
number=browser.find_element_by_id('trainum').text
for i in range(0,len(c2),len(c1)+1):
    xx0.append(c2[i:i+1+len(c1)])
for i in xx0:
    i[5]=i[5]+'\n'+i[6]
    i.pop(6)
xx=pd.DataFrame(data=xx0,
               columns=c1,
               index=range(1,int(number)+1))
print('车票详细信息：')
print(xx)