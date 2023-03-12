# -- coding: utf-8 --**
import requests
import time
import random
import re

id=''      #example:'125797'
site=''    #example:'https://www.zfrontier.com/app/flow/bV0Q8NXdarmB'
cookies='' #WARNING:cookies should be formatted!!!!!
reply_content=''    #feel free


def add_reply(Interval_b,Interval_e):
    global id,site,cookies,reply_content
#Interval_b=5            #最小间隔,单位为秒
#Interval_e=20           #最大间隔,同上

    reply='<p>' + reply_content + '<p>'

    headers={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.zfrontier.com',
        'Origin': 'https://www.zfrontier.com',
        'Referer': site,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'X-CLIENT-LOCALE': 'zh-CN',
        'X-CSRF-TOKEN': '',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data_for_add={
        'time':str(int(time.time())),
        't': '',
        'id':id,
        'action':'add'
        #cancel
    }
    data_for_reply={
        'time':str(int(time.time())),
        't': '',
        'id':id,
        'reply_id':'',
        'content':reply
    }



    add_response = requests.post('https://www.zfrontier.com/api/circle/zanFlow', cookies=cookies, headers=headers, data=data_for_add).text
    add_match_list = re.findall(r'\d+', add_response)
    if add_match_list[0]=='0':
        print('点赞成功!')
    else :
        print('点赞失败!')

    Interval=random.randint(Interval_b,Interval_e)
    print("随机暂停",Interval,"s")
    time.sleep(Interval)

    reply_response = requests.post('https://www.zfrontier.com/v2/flow/reply', cookies=cookies, headers=headers, data=data_for_reply).json
    reply_match_list = re.findall(r'\d+', str(reply_response))
    if reply_match_list[0]=='200':
        print('回复成功!')
    else :
        print('回复失败!')

#examlple:add_reply(1,5)

