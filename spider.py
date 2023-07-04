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
        view_url = 'https://www.zfrontier.com/app/flow/detail/' + article['hash_id']

        #进行去重过滤
        if str(article['id']) in json_str: #如果该抽奖已被存储过则跳过
            print('跳过一个已存储的帖子：',article['hash_id'],'  ('+str(article_cnt)+')')
            article_cnt -= 1
            continue

        cnt = 0 #重试请求次数计数器
        view_headers['Referer'] = view_url
        view_url = 'https://www.zfrontier.com/v2/flow/detail'
        view_data['id'] = article['hash_id']
        response = requests.post(view_url, proxies=proxies,cookies=cookies, headers=view_headers, data=view_data, verify=False).json() # 获取详情
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
            
        if 'lottery' in response['data']['flow'] and response['data']['flow']['lottery'] != None: #如果抽奖信息非空
            if response['data']['flow']['lottery']['status_str'] == '待抽奖':
                temp_lottery_info_dict['lottery_time'] = response['data']['flow']['lottery']['lottery_at'] #开奖时间 格式-> '2023-03-31 20:20'
                temp_lottery_info_dict['jq_flag'] = 'F' #初始化变量“是否需要加群”
                for awards in response['data']['flow']['lottery']['prizesGroup']: #jq_flag存储是否需要加群领奖（值为T或F）
                    if '群' in awards['name'] or check_words(response): #奖品名称中写明需要加群领奖
                        temp_lottery_info_dict['jq_flag'] = 'T'
                        temp_lottery_info_dict['lottery_qq'] = response['data']['flow']['plate']['name'] + ' ' + response['data']['flow']['plate']['qq']  #str格式的抽奖群号+空格+群昵称
                    else:
                        temp_lottery_info_dict['lottery_qq'] = ''
                data_list.append(temp_lottery_info_dict) # 将新的JSON数据添加到Python对象中（存储单个抽奖信息）
                newly_append += 1
                ready_to_send += article['hash_id'] +'  '+ response['data']['flow']['lottery']['lottery_at'] + '\n'
        time.sleep(60)
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

def check_words(response):
    words = ['群内','加群','进群','抽奖','开奖','领奖','在群','群里']
    article_content = response['data']['flow']['item']['article']['text']
    for i in words:
        if i in article_content:
            return True
    else:
        return False


#——————————下方区域为初始化变量——————————#
'使用系统代理设置'
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}

'读取爬取的文章页数'
set_pages_cnt = 2

'读取CK'
cookie_input = 'ZF_CLIENT_ID=1686465249402-12907216653696674; _bl_uid=3qlt8i6krRe1s4vht62wttvfOIh2; user-token=eyJpdiI6Ik4xYjJ6bzZJQ0hnWjdCWEtiYkJ6dUE9PSIsInZhbHVlIjoiM0tIOFh5Q0hZK3B6NlV3TEhJTmp3ajZ6ZGtlaTFDc0RVVUFvRVZxK2d3WlpsZTBpTStaOW9QaHQyRlp4d1h5byIsIm1hYyI6ImM5ODFiOTI5ZDhjYzgwNDgzMGQ3NzVhYTNhMTRlMGNjOWQ0MWMwNWMyY2FkYjkxMjJlY2YwOWE5YzFhOWEyOWUifQ%3D%3D; userDisplayInfo=%7B%22userId%22%3A3832500%2C%22hashId%22%3A%22qO7lmY8L5pEdP%22%2C%22nickname%22%3A%22%E5%8F%AB%E6%88%91%E4%BB%93%E9%BC%A0%22%2C%22avatarPath%22%3A%22%5C%2F%5C%2Fimg.zfrontier.com%5C%2Fava%5C%2F20220529%5C%2Fzf62931cfca88c5%22%2C%22viewUrl%22%3A%22%5C%2Fapp%5C%2Fuser%5C%2FqO7lmY8L5pEdP%22%7D; userServerInfo=eyJpdiI6InNHMk1SOGVVZFd0XC9zY205dENsMkd3PT0iLCJ2YWx1ZSI6IkhVTVBWVXdiZ3p6OFJiMXZlSm8xZ2NBODYxSVRvM1RWeEpzc1d1QmZBTnVIOERaUENSOFFpUWlqOE9OV0JPT1owc1JhK2JhXC82cVVhOFh6UHVZbVwvTHc9PSIsIm1hYyI6IjRiNGY1MDhhNDUwMzUzMjA0MzEwMjExZjU4NDgyNWIwNWFjNjE1NGI3MTIzNDY3NmRhYzBiMTU3YTg2ZTY1OWEifQ%3D%3D'
cookies = cookie_seperator(cookie_input)

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
    'X-CSRF-TOKEN': '1688473073f0d1ed76fb5e4cd3630922818b0a73',
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
    'X-CSRF-TOKEN': '1688473073f0d1ed76fb5e4cd3630922818b0a73',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'time': '1688473074',
    't': '1a1de411c31dbcd7bdd38cfe02b25f97',
    'offset': '',
    'tagIds[0]': '2007',
}

view_data = {
    'time': '1688473074',
    't': '1a1de411c31dbcd7bdd38cfe02b25f97',
    'id': ''
}
pages_cnt = 1    #初始化获取帖子列表页数
article_cnt = -1 #未定义 在spider程序中用于统计这一页获取到的帖子数量
newly_append = 0
ready_to_send = ''


#——————————下方开始主程序——————————#
print('————————————开始获取',set_pages_cnt,'页情报————————————')
while pages_cnt <= set_pages_cnt:
    response = requests.post('https://www.zfrontier.com/v2/home/flow/list', proxies=proxies, cookies=cookies, headers=headers, data=data,verify=False).json()
    article_cnt = len(response['data']['list'])
    print('【爬取第',pages_cnt,'页情报】共获取到',article_cnt,'条帖子信息')
    spider(response,article_cnt) #传入抽奖信息解析函数
    pages_cnt += 1

ready_to_send = '【新增' + str(newly_append) + '条抽奖数据】\n' + ready_to_send
send('【ZF】新增抽奖数据' + str(newly_append) + '条',ready_to_send)

os.startfile(r'C:\Users\Administrator\Desktop\Zfrontier\lottery_info_public\auto_commit.py')
