#此程序为主程序
import configparser
import requests
import json

#下方区域放置所有函数备用
'cookie_seperator函数用于格式化从config.ini中读取到的CK变量备用 【注意】cookie中只应包含值 不要含有中文！'
def cookie_seperator(cookie): 
    cookies = {}
    lst=cookie.split('; ')
    for i in lst:
        temp=i[i.find('=')+1:]
        tmp_index=i[:i.find('=')]
        cookies[tmp_index]=temp
    return cookies
def spider():
    print(pages_cnt)

#下方区域为初始化变量
'读取配置项'
cfp = configparser.RawConfigParser()
cfp.read("config.ini")
'读取CK'
cookie_input = cfp.get("Cookies", "ck")
cookies = cookie_seperator(cookie_input)
'读取爬取的文章页数'
set_pages_cnt=int(cfp.get("Spider", "pages_cnt"))
headers = {
    'Accept': 'application/json, textain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.zfrontier.com',
    'Referer': 'https://www.zfrontier.com/app/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'X-CLIENT-LOCALE': 'zh-CN',
    'X-CSRF-TOKEN': '1677986750b4ca20af6c299d495bc7f1abd334a0',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'time': '1677986751',
    't': '76911247ec209e60fa2d0516b48aa3cc',
    'offset': '',
    'tagIds[0]': 'new',
}
pages_cnt = 1

#下方开始主程序
print('——————开始获取',set_pages_cnt,'页情报——————')
while pages_cnt <= set_pages_cnt:
    response = requests.post('https://www.zfrontier.com/v2/home/flow/list', cookies=cookies, headers=headers, data=data,verify=False).json()
    data['offset'] = response['data']['offset']
    print(data['offset'])
    pages_cnt += 1