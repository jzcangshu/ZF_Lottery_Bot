# -- coding: utf-8 --**
import requests
import time

site='https://www.zfrontier.com/app/'
cookies=''


def check_in():
    global site,cookies


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

    data_for_sign={
        'time':str(int(time.time())),
        't': '',
    }




    check_in_response = requests.post('https://www.zfrontier.com/v2/sign', cookies=cookies, headers=headers, data=data_for_sign).json
    print(check_in_response)





check_in()

