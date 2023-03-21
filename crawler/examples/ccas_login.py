'''
壁虎科技登录;因为是会连续发送多次请求进行数据爬取，所以，我们需要使用requests的session

'''
import requests
import re
import time

def login_V2():
    # headers
    headers = {
        "Referer": "https://bot.91bihu.com/",
        "Connection": "keep-alive"
    }
    # url1-获取token
    url1 = "http://103.36.193.81:8002/ccas/dashboard/login"
    # 发送请求获取响应
    data = {
        "username": "admin",
        "password": "1qaz!QAZ123",
        "captcha": "6n3e1"
    }
    res1 = requests.post(url1, data, headers=headers)
    print(res1)
    print(res1.content)


if __name__ == "__main__":
    login_V2()
