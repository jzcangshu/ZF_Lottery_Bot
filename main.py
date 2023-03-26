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



