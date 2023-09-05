while True: #死循环模式（不定时启动）
	# -- coding: utf-8 --**
	#此程序为参与抽奖主程序
	import requests
	import json
	import os
	import time
	import random
	import datetime
	import re
	import traceback
	from notify import send
	import urllib3
	urllib3.disable_warnings()
	import sys

	#——————————下方区域放置所有函数&全局变量备用——————————#
	def check_network():
		try:
			response = requests.get("https://www.baidu.com")
			if response.status_code == 200:
				return True
			else:
				return False
		except:
			return False

	def check_ZF_access():
		try:
			response = requests.get("https://www.zfrontier.com")
			if response.status_code == 200:
				return True
			else:
				return False
		except:
			return False

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

	'reply_to_lottery函数用于回复参与抽奖'
	def reply_to_lottery(id,hash_id):
		global reply_failure_count , ready_to_send 
		'初始化回复帖子所用到的headers & data'
		headers={
			'Accept': 'application/json, text/plain, */*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
			'Connection': 'keep-alive',
			'Content-Length': '',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Host': 'www.zfrontier.com',
			'Origin': 'https://www.zfrontier.com',
			'Referer': 'waiting 4 initializing',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
			'X-CLIENT-LOCALE': 'zh-CN',
			'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
		}
		data_for_reply={
			'time':str(int(time.time())),
			't': '',
			'id': str(id),
			'reply_id':'',
			'content':'waiting 4 initializing'
		}

		site = 'https://www.zfrontier.com/app/flow/' + hash_id
		reply_content = random.choice(accounts['chat'])
		reply='<p>' + reply_content + '<p>'
		headers['Referer'] = site
		headers['User-Agent'] = UA
		data_for_reply['content'] = reply
	#    add_response = requests.post('https://www.zfrontier.com/api/circle/zanFlow', cookies=cookies, headers=headers, data=data_for_add).text
	#    add_match_list = re.findall(r'\d+', add_response)
	#    if add_match_list[0]=='0':
	#        print('点赞成功!')
	#    else :
	#        print('点赞失败!')
		# 回复帖子
		try:
			reply_response = requests.post('https://www.zfrontier.com/v2/flow/reply', cookies=cookies, headers=headers, data=data_for_reply, proxies=proxies, verify=False).json
			reply_match_list = re.findall(r'\d+', str(reply_response))
			if reply_match_list[0]=='200':
				return True  #回复成功
			else:
				reply_failure_count += 1
				return False #回复失败
		except requests.exceptions.RequestException as e:
			# 处理请求异常，例如连接问题、超时、ip被ban等
			return False
		except Exception as e:
			# 处理其他异常，如JSON解析错误等
			raise Exception(str(e))			
			#其他未知bug直接raise
		
	'message变量存储所有账号的私信信息'
	message = ''
	'message_flag用于存储本轮是否查询到新的私信'
	message_flag = False
	'qq_add用于存储本轮中需要被推送加群的QQ群'
	qq_add = ''
	'qualified_qq存储所有已经添加过的QQ群用于查重，减少推送量'
	check_file = open('qualified_qq.txt','a', encoding="UTF-8")
	check_file.close() #防止文件不存在，否则创建
	check_file = open('checked_ids.txt','a', encoding="UTF-8")
	check_file.close() #防止文件不存在，否则创建
	qq = open('qualified_qq.txt','r', encoding="UTF-8")
	qualified_qq = qq.read()
	qq.close()
	ids = open('checked_ids.txt','r', encoding="UTF-8")
	message_ids = ids.read()
	ids.close()

	#——————————下方开始主程序——————————#
	try:
		with open('config.json', 'r', encoding="UTF-8") as f:
			config = json.load(f)
			
		ready_to_send=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ' 开始任务…… \n'
	except Exception as e:
		traceback.print_exception(e)
		wait_for_it = input('【致命错误断点】Press enter to close the terminal window')   


	try:
		'have_engaged参数用于判断单个账号是否在本轮抽奖中参与了抽奖，如果没有需要参与的则跳过该账号以节省时间'
		have_engaged = False
		warning_text = ''
		'全局参与抽奖计数器，用于判断本轮大循环是否没有进行过任何抽奖。若未参与任何新抽奖，则延迟5小时后再次检测'
		total_engage_count = 0
		for accounts in config:
			#——————————下方区域为初始化变量——————————#
			'have_sent用于判断是否已经因为异常中断发送过一次抽奖日志，避免重复发送'
			have_sent = False
			'flag变量用于重试检测是否能够获取到抽奖数据JSON'
			flag = False
			'lottery_info.json 文件地址'
			api = 'https://raw.githubusercontent.com/jzcangshu/lottery_info_public/master/lottery_info.json'

			'回复失败计数器，用来判断账号是否失效'
			reply_failure_count = 0
			'分别用于判断本机网络是否正常/本机IP能否正常访问ZF'
			network_failure = False
			ZF_access_failure = False
			'参与成功抽奖计数器'
			success_lottery_count = 0
			'本轮新增过期抽奖计数器'
			overtime_lottery_count = 0

			'读取单个账号信息'
			account_num = accounts['num'] #读取账号编号
			account_notice = accounts['notice'] #读取账号备注名称
			reply_waiting = accounts['reply_waiting'] #读取账号回复延迟（上下浮动50%）
			cookie_input = accounts['cookies'] #读取对应CK
			cookies = cookie_seperator(cookie_input) #格式化CK
			UA = accounts['UA'] #读取UserAgent
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
				print("未找到cookies,下一个!")
				ready_to_send+="未找到cookies,下一个!\n"
				continue
			if http_proxy:
				proxies['http']=http_proxy
			if https_proxy:
				proxies['https']=https_proxy

			if have_engaged: #如果上一个账号参与过了抽奖
				if waiting_before_use:
					print(">>>>>>>>>>>>账号间隔",waiting_before_use,"秒<<<<<<<<<<")
					time.sleep(int(waiting_before_use))
				else:
					Interval=random.randint(60,600)
					print("未填入暂停时间，随机暂停",Interval,"秒")
					time.sleep(Interval)
			have_engaged = False


			#————————————开始检查私信————————————#
			#message_list = requests.post('https://www.zfrontier.com/v2/notifies', cookies=cookies, headers=headers, data=data_for_reply, proxies=proxies, verify=False).json
			#——————————开始单个账号抽奖——————————#
			'''
			①登录账号 输出昵称 检查签到
			②拉取GitHub上存储的lottery_info.json
			③解析抽奖信息JSON文件,与/dyids/1.txt进行比对查重 (按照账号编号区分文件)
			④lottery_time_checker检查是否超过开奖时间
			④通过查重+开奖时间检测的 -> 调用reply函数参与抽奖+写入dyids(放弃点赞判断减少风控风险,但是留着这功能作为可选项,具体参考闪米特同款)
			⑤根据lottery_info.json中的加群信息判断是否需要加群 -> qualified_qq.txt加群查重 -> 添加加群信息到待推送str中(一行一个)
			⑥所有账号运行结束后统一进行加群推送
			'''
			print('▶账号'+str(account_num)+'开始抽奖\n')
			ready_to_send += '▶账号'+str(account_num)+'开始抽奖'+'('+account_notice+')\n'
			for cnt in range(20):
				try:
					print('开始获取公共API抽奖数据...\n')
					response = requests.get(api, proxies=proxies, verify=False, timeout=5)
					if response.status_code == 200:
						lottery_data_json = json.loads(response.text)
						flag = True
						break
				except:
					print('【严重错误】获取公共抽奖数据失败,请检查你是否能够正常访问GitHub!')
					time.sleep(30)
					print('自动重试（' + str(cnt+1) + '）...')
			if flag == False:
				print('【严重错误】尝试获取抽奖数据20次失败，开始推送错误')
				content = '【新增Q群】\n'+qq_add + '————————————————————————————\n' + '【运行日志】\n' + ready_to_send
				content += '抽奖数据获取失败，任务已被终止\n'
				send('【ZF】⁉抽奖被中断⁉',content)
				have_sent = True
				break
			
			# 检测是否存在账号对应的dyid文件，如果没有则创建
			dyid_file = open('./dyids/dyids'+str(account_num)+'.txt','a+')
			dyid_file.close()
			# 读取并存储dyid文件中已有的dyids数据（逗号分隔）
			dyid_file = open('./dyids/dyids'+str(account_num)+'.txt','r', encoding="UTF-8") 
			dyids = dyid_file.read()
			dyid_file.close()
			# 遍历抽奖数据文件
			for data in lottery_data_json:
				# 获取单个抽奖帖子的所有信息
				lottery_id = data['id']
				lottery_hash_id = data['hash_id']
				lottery_time = data['lottery_time']
				lottery_qq = data['lottery_qq']
				lottery_jq_flag = False

				if lottery_hash_id in dyids: # 已参与的抽奖
					continue
				else:
					if lottery_time_checker(lottery_time): #判断是否已经开奖
						if reply_to_lottery(lottery_id,lottery_hash_id): #如果回复成功
							have_engaged = True
							print('[参与成功]'+'https://www.zfrontier.com/app/flow/'+str(lottery_hash_id))
							Interval=random.randint(reply_waiting//2 , reply_waiting+reply_waiting//2) #回复延迟上下浮动50%
							print("——————————•随机暂停",Interval,"秒•——————————")
							time.sleep(Interval)
							#写入对应的dyids
							dyids += lottery_hash_id + ','
							success_lottery_count += 1
							#全局参与数+1
							total_engage_count += 1

							if data['jq_flag'] == 'T':
								lottery_jq_flag = True
							#如果抽奖要求加群 并且 本轮所有账号的抽奖中都还未涉及过添加此群 并且 该群未出现在已添加的群聊中(qualified_qq.txt) -> 加入加群推送STR
							if lottery_jq_flag and (lottery_qq not in qq_add) and (lottery_qq not in qualified_qq):
								qq_add += lottery_qq + '\n'
								qualified_qq += lottery_qq + ','
						
						else:   
							reply_failure_count += 1#若新增抽奖记录刚好在3条之内，if语句无法被触发，这部分又该怎么改呢？（解铃还须系铃人，没啥思路
							if reply_failure_count >= 3:				  #👆有了，不如在回复之前每次先ping一下？
								if check_network():						  #👆👆那会不会因为请求太过于频繁而更容易被封号被ban ip？我不到啊🤔
									temp_warining_text = '账号'+str(account_num)+'已失效！'+'('+account_notice+')'
									if not check_ZF_access():
										temp_warining_text = '本机IP被ZF临时风控，抽奖中断！'
										warning_text += temp_warining_text+'\n'
										content =warning_text+'\n' '【新增Q群】\n'+qq_add
										send('【ZF】⁉抽奖被中断⁉',content)						#加点符号增加警示；这应该也算中断吧
										have_sent = True
										sys.exit(0)
									warning_text += temp_warining_text+'\n'
									continue
								else:
									while True:
										print('网络连接中断，10min后重试')
										time.sleep(600)
										if check_network():
											break
							ready_to_send += '[参与失败]'+'https://www.zfrontier.com/app/flow/'+str(lottery_hash_id)+'\n'
							print('[参与失败]'+'https://www.zfrontier.com/app/flow/'+str(lottery_hash_id))
							Interval=random.randint(reply_waiting//2 , reply_waiting+reply_waiting//2) #回复延迟上下浮动50%
							print("随机暂停",Interval,"秒")
							time.sleep(Interval)
					else:
						print('[过期抽奖]'+'https://www.zfrontier.com/app/flow/'+str(lottery_hash_id))
						#写入dyids，下次就不会再理会此帖了。防止过期抽奖长期滞留
						dyids += lottery_hash_id + ','
						overtime_lottery_count += 1
			dyid_file = open('./dyids/dyids'+str(account_num)+'.txt','w', encoding="UTF-8") 
			dyid_file.write(dyids)
			dyid_file.close()
			'开始记录该账号本轮抽奖状态'
			ready_to_send += '  ✅成功参与' + str(success_lottery_count) + '条 ' + '❎参与失败' + str(overtime_lottery_count) + '条\n'

		#存储本轮所有账号筛选出的需添加的QQ群为已经添加
		qq = open('qualified_qq.txt','r+', encoding="UTF-8")
		qq.write(qualified_qq)
		qq.close()

		if not have_sent:
			#推送qq_add变量（需要添加的QQ群号）  和   ready_to_send变量（日志）
			content = warning_text+'【新增Q群】\n'+qq_add + '————————————————————————————\n' + '【运行日志】\n' + ready_to_send
			send('【ZF】抽奖日志',content)
		
	except Exception as e:
		traceback.print_exception(e)
		send('【ZF】⁉抽奖被中断⁉','脚本运行出现bug,请进行排查😢以下是报错信息:\n' + str(e))	   #不知道该不该添加新增qq群和之前运行正常时的信息
		#wait_for_it = input('【致命错误断点】Press enter to close the terminal window')    
		#在这里直接退出程序会不会更符合使用场景,毕竟是未考虑到的运行错误，同时减少资源开销(?)
		exit(0)
	
	time.sleep(random.randint(43200,129600)) 
	#请按个人口味酌情添加
