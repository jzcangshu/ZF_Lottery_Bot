# -- coding: utf-8 --**
#此程序为参与抽奖主程序
import configparser
import requests
import json
import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import random

#——————————下方区域放置所有函数备用——————————#
'cookie_seperator函数用于格式化从config.ini中读取到的CK变量备用 【注意】cookie中只应包含值 不要含有中文！'
def cookie_seperator(cookie): 
    cookies = {}
    lst=cookie.split('; ')
    for i in lst:
        temp=i[i.find('=')+1:]
        tmp_index=i[:i.find('=')]
        cookies[tmp_index]=temp
    return cookies

'lottery_time_checker函数用于判断读取到的抽奖数据文件中的单个帖子开奖日期与当前日期的关系,如果还未到开奖时间则返回True,否则返回False'
def lottery_time_checker(lottery_at):
    # 获取当前时间
    current_time = time.localtime()
    # 输出当前时间的年份
    year = str(current_time.tm_year)
    # 输出当前时间的月份
    month = current_time.tm_mon
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    # 输出当前时间的日期
    day = current_time.tm_mday
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    # 输出当前时间的小时数
    hour = current_time.tm_hour
    if hour < 10:
        hour = '0' + str(hour)
    else:
        hour = str(hour)
    # 输出当前时间的分钟数
    min = current_time.tm_min
    if min < 10:
        min = '0' + str(min)
    else:
        min = str(min)
    os_time = year + '-' + month + '-' + day + ' ' + hour + ':' + min
    still_lottery = os_time < lottery_at #返回True则还未开奖
    return(still_lottery)


#推送先不急

#——————————下方开始主程序——————————#
with open('0.json', 'r') as f:
    config = json.load(f)
    
ready_to_send='开始任务…… \n'
    
for accounts in config:
    #——————————下方区域为初始化变量——————————#
    '读取CK'
    cookie_input = accounts['cookies']
    cookies = cookie_seperator(cookie_input)
    proxies = {
            'http': os.environ.get('HTTP_PROXY'),
            'https': os.environ.get('HTTPS_PROXY')
    }    
    #不填则使用系统代理
    http_proxy = accounts.get('HTTP_PROXY', '')
    https_proxy = accounts.get('HTTPS_PROXY', '')
    waiting_before_use = accounts.get('WAITING_BEFORE_USE', '')
    # 如果cookies为空，则跳过当前循环
    if not cookies:
        print("未找到cookies，下一个！")        #其实应该再检测是否有下一个账号，没时间啦
        ready_to_send+="未找到cookies，下一个！\n"
        continue
    if http_proxy:
        proxies['http']=http_proxy
    if https_proxy:
        proxies['https']=https_proxy
    if waiting_before_use:
        print("随机暂停",waiting_before_use,"s")
        time.sleep(waiting_before_use)
    else :
        Interval=random.randint(60,600)
        print("未填入暂停时间，随机暂停",Interval,"s")
        time.sleep(Interval)


    #顺带把想到的写一下
    #——————————最开始先尝试登录，若成功则输出昵称——————————#


    
    #随机取出chat中元素并评论：
    content = random.choice(accounts['chat'])



