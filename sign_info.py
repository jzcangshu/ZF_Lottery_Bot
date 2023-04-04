#-*- coding: UTF-8-*-
import requests
import time
import json

def sign_info():
    global id,cookies,ready_to_send
    headers_for_getsigninfo={
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.zfrontier.com",
        "Origin": "https://www.zfrontier.com",
        "Referer": "https://www.zfrontier.com/",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
        "X-CLIENT-LOCALE": "zh-CN",
        "X-CSRF-TOKEN": "",
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data={
        'time':str(int(time.time())),
        't': '',
    }
    response = requests.post('https://www.zfrontier.com/v2/signInfo', cookies=cookies, headers=headers_for_getsigninfo, data=data)
    sgif=json.loads(response.text)
    if sgif["ok"]==0:
        check_state=sgif['data']['sign_info']['desc']
        if check_state[0:5]=='已连续签到':
            ct='今日已签到'                                                    #这里可加标识来辨别是否已签到的变量
        else :
            ct='今日未签到'
        content='登陆成功！用户组：'+ str(sgif["data"]["lv_str"]) + ',' + \
            '等级：' + str(sgif["data"]["bbs_lv"]) + ','+ \
            '总积分:' + str(sgif["data"]["bbs_score"]) + ',' + \
            '签到状态:' + ct + '\n'
        ready_to_send+=content                                              
        print(content)
    else:
        print('签到失败！')
