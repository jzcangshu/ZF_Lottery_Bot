# 该文件用于手动输入cookie并模拟登录 获取一页情报页面文章数据

import requests
import time

def cookie_seperator(cookie):
    cookies = {}
    lst=cookie.split('; ')
    for i in lst:
        temp=i[i.find('=')+1:]
        tmp_index=i[:i.find('=')]
        cookies[tmp_index]=temp
    return cookies

cookie_input=input('请输入cookie，')
cookies = cookie_seperator(cookie_input) #格式化cookies

headers = {
    'Accept': 'application/json, textain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'ZF_CLIENT_ID=1677983223183-5275536195173502; _bl_uid=j6la1eC2u4zr3Fvqvyz7oq9hFqzF; user-token=eyJpdiI6IndIWkRzUUlmbTJmNVNvSEZ1d1U5aXc9PSIsInZhbHVlIjoiRStYWDhYVnhubmpCODFYaDFqd293MWxHTEdwdmJDT1FjUHNjcE5UclJBVVNkTURuUDBtUncxWHVOeUZIZmM1cCIsIm1hYyI6IjliNTNkMjIwODkzYjhmZGQ1YzgwNjZjNjdmOTFiMjYyNzliMjcxNzJiYzZjNWVmOGUzY2JiZDNiNjU2NmEwYjgifQ%3D%3D; userDisplayInfo=%7B%22userId%22%3A3755695%2C%22hashId%22%3A%22dDWyjldWrZ6wzO%22%2C%22nickname%22%3A%22%E5%B0%8FDXG%22%2C%22avatarPath%22%3A%22%5C%2F%5C%2Fimg.zfrontier.com%5C%2Favatar%5C%2F211214%5C%2Fava61b8b528b3b7d%22%2C%22viewUrl%22%3A%22%5C%2Fapp%5C%2Fuser%5C%2FdDWyjldWrZ6wzO%22%7D; userServerInfo=eyJpdiI6ImpIWGY3OTF3Zjc0ekNqMGRCRlRXSWc9PSIsInZhbHVlIjoiMlZVcjFsa2ZoXC9weTJaelBJTHFCOWZXckJzb09Tc3VrTVhybkxrWGtSWk5hYWcyUW5mWWROMThpbWJuMmxZNzdSR0thUEFoaTY1T1VIc25VNytcL2JZQT09IiwibWFjIjoiZTJlM2VlZDYxNDVhNDkxYzQ5OWE1NDhjZTM0MDVlYzg5N2RiNzBiNTdlMjdhMTMwYWNiZTQ3YThlZmRhNWRjYSJ9',
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

response = requests.post('https://www.zfrontier.com/v2/home/flow/list', cookies=cookies, headers=headers, data=data).json()
print(response)
