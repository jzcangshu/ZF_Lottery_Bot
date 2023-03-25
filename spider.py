# -- coding: utf-8 --**
#此程序为后端爬取抽奖程序
import configparser
import requests
import json
import time

#——————————下方区域放置所有函数备用——————————#
'spider函数用于解析list中获取到的文章信息并存储（list内无法判断是否含有抽奖信息）'
def spider(r):
    temp_lottery_info_lst = []
    temp_lottery_info_str = ''
    with open('lottery_info.txt','a+') as f:
        for article in r['data']['list']: #开始获取单个帖子详情
            id = article['id']
            hash_id = article['hash_id']
            view_url = 'https://www.zfrontier.com/v2/flow/detail/' + hash_id
            view_headers['Referer'] = view_url
            view_headers['X-CSRF-TOKEN'] = ''
            response = requests.post(view_url,cookies=cookies, headers=view_headers, data=data,verify=False).json() # 获取详情
            if response['data']['flow']['lottery'] != None: #如果抽奖信息非空
                if response[data]['flow']['lottery']['status_str'] == '待抽奖':
                    lottery_time = response['data']['flow']['lottery']['lottery_at'] #获取开奖时间
                    temp_lottery_info_str = str(id) + ',' + str(hash_id) + ',' + str(lottery_time) + '\n'
                    temp_lottery_info_lst.append(temp_lottery_info_str)
                    f.writelines(temp_lottery_info_lst) #将被筛选出来的抽奖信息写入TXT文件
            time.sleep(5)

'cookie_seperator函数用于格式化从config.ini中读取到的CK变量备用 【注意】cookie中只应包含值 不要含有中文！'
def cookie_seperator(cookie): 
    cookies = {}
    lst=cookie.split('; ')
    for i in lst:
        temp=i[i.find('=')+1:]
        tmp_index=i[:i.find('=')]
        cookies[tmp_index]=temp
    return cookies


#——————————下方区域为初始化变量——————————#
cfp = configparser.RawConfigParser()
cfp.read("config.ini")
'读取CK'
cookie_input = cfp.get("Cookies", "ck")
cookies = cookie_seperator(cookie_input)
'读取爬取的文章页数'
set_pages_cnt=3
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

view_headers = headers #用于获取文章详情的headers，区别在于无X-CSRF-TOKEN并修改了Referer

data = {
    'time': '1677986751',
    't': '76911247ec209e60fa2d0516b48aa3cc',
    'offset': '',
    'tagIds[0]': '2007',
}
pages_cnt = 1



#——————————下方开始主程序——————————#
print('——————开始获取',set_pages_cnt,'页情报——————')
while pages_cnt <= set_pages_cnt:
    response = requests.post('https://www.zfrontier.com/v2/home/flow/list', cookies=cookies, headers=headers, data=data,verify=False).json()
    print(response)
    data['offset'] = response['data']['offset']
    print('第',pages_cnt,'页数据获取完成')
    spider(response) #传入抽奖信息解析函数
    pages_cnt += 1
