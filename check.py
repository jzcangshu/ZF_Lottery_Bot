#此程序为中奖者检查程序
import requests
import json
import os
import time
import urllib3
urllib3.disable_warnings()
from notify import send

'读取爬取的文章页数，在这里设置检查的开奖帖子页数'
set_pages_cnt = 25
#——————————下方区域放置所有函数备用——————————#
def cookie_seperator(cookie): 
    cookies = {}
    lst=cookie.split('; ')
    for i in lst:
        temp=i[i.find('=')+1:]
        tmp_index=i[:i.find('=')]
        cookies[tmp_index]=temp
    return cookies

'spider函数用于解析list中获取到的文章信息并检查中奖者'
def spider(r,article_cnt):
    global ready_to_send
    global accounts_hash_list
    global checked_ids
    global got_new_award
    for article in r['data']['list']: # 开始获取单个帖子详情
        temp_lottery_info_dict = {}   # 存储单个帖子中的抽奖信息
        temp_lottery_info_dict['id'] = article['id']
        temp_lottery_info_dict['hash_id'] = article['hash_id']
        view_url = 'https://www.zfrontier.com/v2/flow/detail/' + article['hash_id']

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
            
        if 'lottery' in response['data']['flow'] and response['data']['flow']['lottery'] != None: #如果抽奖信息非空
            if response['data']['flow']['lottery']['status_str'] == '已结束':
                prizesGroup = response['data']['flow']['lottery']['prizesGroup']
                for prizeGroup in prizesGroup:
                    for award in prizeGroup['list']:
                        award_id = str(award['id']) #每份奖品对应的数字id
                        award_name = award['name'] #奖品名
                        reward_user_hash = award['rewardUser']['hash_id']
                        if reward_user_hash in accounts_hash_list and award_id not in checked_ids: #中奖者为本地config中的用户且该奖品此前未被记录过
                            notice_word = accounts_hash_list[reward_user_hash] + '中奖了,奖品：' + award_name + '\n' #生成中奖提示推送信息
                            ready_to_send += notice_word
                            print(notice_word)
                            checked_ids += award_id + ','
                            got_new_award = True
                        else:
                            print('未中奖！')
            else:
                print('未开奖帖子')
        else:
            print('无抽奖帖子')
        time.sleep(15)


def get_user_hash(s):
    n = len(s)
    # 构建后缀数组
    suffixes = sorted(range(n), key=lambda i: s[i:])
    ranks = [0] * n
    for i in range(1, n):
        ranks[suffixes[i]] = ranks[suffixes[i-1]] + (s[suffixes[i-1]:] != s[suffixes[i]:])
    # 使用 Kasai 算法构建 LCP 数组
    lcp = [0] * (n-1)
    h = 0
    for i in range(n):
        if ranks[i] == 0:
            continue
        j = suffixes[ranks[i]-1]
        while i+h < n and j+h < n and s[i+h] == s[j+h]:
            h += 1
        lcp[ranks[i]-1] = h
        if h > 0:
            h -= 1
    # 找到 LCP 最大的位置
    max_lcp_index = max(range(n-1), key=lambda i: lcp[i])
    temp = s[suffixes[max_lcp_index]:suffixes[max_lcp_index]+lcp[max_lcp_index]]
    hash = temp[:-4]
    return hash


#——————————下方区域为初始化变量——————————#
got_new_award = False #表示本轮检测是否有新增中奖
ready_to_send = ''
accounts_hash_list = {}
'使用系统代理设置'
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}

'读取CK'
cookie_input = 'ZF_CLIENT_ID=1677983223183-5275536195173502; _bl_uid=j6la1eC2u4zr3Fvqvyz7oq9hFqzF; user-token=eyJpdiI6IndIWkRzUUlmbTJmNVNvSEZ1d1U5aXc9PSIsInZhbHVlIjoiRStYWDhYVnhubmpCODFYaDFqd293MWxHTEdwdmJDT1FjUHNjcE5UclJBVVNkTURuUDBtUncxWHVOeUZIZmM1cCIsIm1hYyI6IjliNTNkMjIwODkzYjhmZGQ1YzgwNjZjNjdmOTFiMjYyNzliMjcxNzJiYzZjNWVmOGUzY2JiZDNiNjU2NmEwYjgifQ%3D%3D; userDisplayInfo=%7B%22userId%22%3A3755695%2C%22hashId%22%3A%22dDWyjldWrZ6wzO%22%2C%22nickname%22%3A%22%E5%B0%8FDXG%22%2C%22avatarPath%22%3A%22%5C%2F%5C%2Fimg.zfrontier.com%5C%2Favatar%5C%2F211214%5C%2Fava61b8b528b3b7d%22%2C%22viewUrl%22%3A%22%5C%2Fapp%5C%2Fuser%5C%2FdDWyjldWrZ6wzO%22%7D; userServerInfo=eyJpdiI6Im1ZY1lqMTZzZEcxb1R0Z3ZrcWdDVFE9PSIsInZhbHVlIjoib2hNK2s0dXZJeHAyXC96K2xZSTNEdTBiME43WHJBd3M1N2h5WDZDZHRcL3E0WGQ1MzlBU3M2MXFUTnZvd2hWenZ0dTM0bVNiRUxOSkx3a0NSUnJOYXNFZz09IiwibWFjIjoiYmFhOTVkNDI1Mjk4ZGJmMWE5YjAzNGNhMjlkNzQyMjVlMjNlNGZlNmI4NTEyYjk5MDM0ZmE2NGI2YTlhY2JjNSJ9'
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



try:
	with open('config.json', 'r', encoding="UTF-8") as f:
		config = json.load(f)
	f.close()
	for accounts in config:
		'读取单个账号信息'
		account_num = str(accounts['num']) #读取账号编号(str格式)
		account_notice = accounts['notice'] #读取账号备注名称
		if len(account_notice) == 0:
			account_notice = '账号'+account_num

		ck = accounts['cookies']
		hash = get_user_hash(ck)
		accounts_hash_list[hash] = account_notice #把每个账号的hash加入到列表中 便于后续比对中奖者
	check_file = open('checked_id.txt','a') #检查文件是否存在，否则创建
	check_file.close()
	with open('checked_id.txt', 'r', encoding="UTF-8") as f:
		checked_ids = f.readline()
	f.close()


	#——————————下方开始主程序——————————#
	
	print('————————————开始检查',set_pages_cnt,'页中奖————————————')
	while pages_cnt <= set_pages_cnt:
		response = requests.post('https://www.zfrontier.com/v2/home/flow/list', proxies=proxies, cookies=cookies, headers=headers, data=data,verify=False).json()
		data['offset'] = response['data']['offset']
		article_cnt = len(response['data']['list'])
		print('【检查第',pages_cnt,'页中奖】共获取到',article_cnt,'条帖子信息')
		spider(response,article_cnt) #传入抽奖信息解析函数
		pages_cnt += 1

	with open('checked_id.txt', 'w', encoding="UTF-8") as f:
		f.write(checked_ids)
	f.close()

	print(ready_to_send)

	if got_new_award == True: #推送中奖信息
		send('【ZF】有账号中奖了！',ready_to_send)


except Exception as e:
    traceback.print_exception(e)
    wait_for_it = input('【致命错误断点】Press enter to close the terminal window')
