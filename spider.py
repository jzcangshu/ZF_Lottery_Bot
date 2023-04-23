# -- coding: utf-8 --**
#此程序为后端爬取抽奖程序
import configparser
import requests
import json
import time
import os
import urllib3
urllib3.disable_warnings()
from notify import send

#——————————下方区域放置所有函数备用——————————#
'spider函数用于解析list中获取到的文章信息并存储(list内无法判断是否含有抽奖信息)'
def spider(r,article_cnt):
    global newly_append
    global ready_to_send
    f = open('lottery_info.json','r', encoding="UTF-8")
    json_str = f.read()               # 读取文件中原有的抽奖数据
    f.close()

    if len(json_str) == 0:            #如果文件为空则需要初始化JSON格式
        json_str = '[]'
    data_list = json.loads(json_str)  # 将JSON数据解析为Python列表


    for article in r['data']['list']: # 开始获取单个帖子详情
        temp_lottery_info_dict = {}   # 存储单个帖子中的抽奖信息
        temp_lottery_info_dict['id'] = article['id']
        temp_lottery_info_dict['hash_id'] = article['hash_id']
        view_url = 'https://www.zfrontier.com/v2/flow/detail/' + article['hash_id']

        #进行去重过滤
        if str(article['id']) in json_str: #如果该抽奖已被存储过则跳过
            print('跳过一个已存储的帖子：',article['hash_id'],'  ('+str(article_cnt)+')')
            article_cnt -= 1
            continue

        cnt = 0 #重试请求次数计数器
        view_headers['Referer'] = view_url
        response = requests.post(view_url, proxies=proxies,cookies=cookies, headers=view_headers, data=data, verify=False).json() # 获取详情
        while cnt<= 3 and ( response['msg'] == '操作太频繁了' or response['data'] == []):
            cnt += 1
            print('【风控警告】自动暂停',str(60*cnt),'秒...')
            time.sleep(60*cnt)
            response = requests.post(view_url, proxies=proxies,cookies=cookies, headers=view_headers, data=data, verify=False).json() # 获取详情
        if response['msg'] == '操作太频繁了' or response['data'] == []:
            return('【风控警告】超出最大风控重试次数限制，程序强制退出')
        # 循环重试最多3次
        
        print('成功获取帖子详情：',article['hash_id'],'  ('+str(article_cnt)+')')
        article_cnt -= 1
            
        if response['data']['flow']['lottery'] != None: #如果抽奖信息非空
            if response['data']['flow']['lottery']['status_str'] == '待抽奖':
                temp_lottery_info_dict['lottery_time'] = response['data']['flow']['lottery']['lottery_at'] #开奖时间 格式-> '2023-03-31 20:20'
                temp_lottery_info_dict['jq_flag'] = 'F' #初始化变量“是否需要加群”
                for awards in response['data']['flow']['lottery']['prizesGroup']: #jq_flag存储是否需要加群领奖（值为T或F）
                    if '群' in awards['name']: #奖品名称中写明需要加群领奖
                        temp_lottery_info_dict['jq_flag'] = 'T'
                        temp_lottery_info_dict['lottery_qq'] = response['data']['flow']['plate']['name'] + ' ' + response['data']['flow']['plate']['qq']  #str格式的抽奖群号+空格+群昵称
                    else:
                        temp_lottery_info_dict['lottery_qq'] = ''
                data_list.append(temp_lottery_info_dict) # 将新的JSON数据添加到Python对象中（存储单个抽奖信息）
                newly_append += 1
                ready_to_send += article['hash_id'] +'  '+ response['data']['flow']['lottery']['lottery_at'] + '\n'
        time.sleep(15)
    json_str = json.dumps(data_list)         # 将Python对象转换为JSON格式的字符串

    f = open('lottery_info.json','w', encoding="UTF-8")
    f.write(json_str)                        # 将被筛选出的抽奖帖子信息写回到.json文件中(包括原有的)

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
'使用系统代理设置'
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}

'读取CK'
cookie_input = 'ZF_CLIENT_ID=1677983223183-5275536195173502; _bl_uid=j6la1eC2u4zr3Fvqvyz7oq9hFqzF; user-token=eyJpdiI6IndIWkRzUUlmbTJmNVNvSEZ1d1U5aXc9PSIsInZhbHVlIjoiRStYWDhYVnhubmpCODFYaDFqd293MWxHTEdwdmJDT1FjUHNjcE5UclJBVVNkTURuUDBtUncxWHVOeUZIZmM1cCIsIm1hYyI6IjliNTNkMjIwODkzYjhmZGQ1YzgwNjZjNjdmOTFiMjYyNzliMjcxNzJiYzZjNWVmOGUzY2JiZDNiNjU2NmEwYjgifQ%3D%3D; userDisplayInfo=%7B%22userId%22%3A3755695%2C%22hashId%22%3A%22dDWyjldWrZ6wzO%22%2C%22nickname%22%3A%22%E5%B0%8FDXG%22%2C%22avatarPath%22%3A%22%5C%2F%5C%2Fimg.zfrontier.com%5C%2Favatar%5C%2F211214%5C%2Fava61b8b528b3b7d%22%2C%22viewUrl%22%3A%22%5C%2Fapp%5C%2Fuser%5C%2FdDWyjldWrZ6wzO%22%7D; userServerInfo=eyJpdiI6Im1ZY1lqMTZzZEcxb1R0Z3ZrcWdDVFE9PSIsInZhbHVlIjoib2hNK2s0dXZJeHAyXC96K2xZSTNEdTBiME43WHJBd3M1N2h5WDZDZHRcL3E0WGQ1MzlBU3M2MXFUTnZvd2hWenZ0dTM0bVNiRUxOSkx3a0NSUnJOYXNFZz09IiwibWFjIjoiYmFhOTVkNDI1Mjk4ZGJmMWE5YjAzNGNhMjlkNzQyMjVlMjNlNGZlNmI4NTEyYjk5MDM0ZmE2NGI2YTlhY2JjNSJ9'
cookies = cookie_seperator(cookie_input)

'读取爬取的文章页数'
set_pages_cnt = 3

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

#view_headers 用于获取文章详情的headers，区别在于无X-CSRF-TOKEN并修改了Referer
view_headers = {
    'Accept': 'application/json, textain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.zfrontier.com',
    'Referer': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'X-CLIENT-LOCALE': 'zh-CN',
    'X-CSRF-TOKEN': '',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


data = {
    'time': '1677986751',
    't': '76911247ec209e60fa2d0516b48aa3cc',
    'offset': '',
    'tagIds[0]': '2007',
}
pages_cnt = 1    #初始化获取帖子列表页数
article_cnt = -1 #未定义 在spider程序中用于统计这一页获取到的帖子数量
newly_append = 0
ready_to_send = ''


#——————————下方开始主程序——————————#
print('————————————开始获取',set_pages_cnt,'页情报————————————')
while pages_cnt <= set_pages_cnt:
    response = requests.post('https://www.zfrontier.com/v2/home/flow/list', proxies=proxies, cookies=cookies, headers=headers, data=data,verify=False).json()
    data['offset'] = response['data']['offset']
    article_cnt = len(response['data']['list'])
    print('【爬取第',pages_cnt,'页情报】共获取到',article_cnt,'条帖子信息')
    spider(response,article_cnt) #传入抽奖信息解析函数
    pages_cnt += 1

ready_to_send = '【新增' + str(newly_append) + '条抽奖数据】\n' + ready_to_send
send('ZF_Lottery_Spider新增抽奖数据',ready_to_send)

os.startfile(r'C:\Users\Administrator\Desktop\Zfrontier\lottery_info_public\auto_commit.py')
