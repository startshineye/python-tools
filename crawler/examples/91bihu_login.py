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
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    # url1-获取token
    url1 = "https://bot.91bihu.com/identity/api/v1/Login/LoginApi2"
    # 发送请求获取响应
    login_data = {
        "client_id": "bot",
        "client_secret": "secret",
        "grant_type": "password",
        "password": "xunjie031228",
        "scope": "employee_center car_business smart_car_mgts",
        "username": "xjhy3"
    }
    res1 = requests.post(url1, json=login_data, headers=headers)
    print(res1)
    print(res1.content)


def login():
    # session
    session = requests.session()
    # headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    # url1-获取token
    url1 = "https://bot.91bihu.com/identity/api/v1/Login/LoginApi2"
    # 发送请求获取响应
    login_data = {
        "client_id": "bot",
        "client_secret": "secret",
        "grant_type": "password",
        "password": "xunjie031228",
        "scope": "employee_center car_business smart_car_mgts",
        "username": "xjhy3"
    }

    res1 = session.post(url1, data=login_data, headers=headers)
    print(res1.text)
    # 正则获取token里面的值
    # token = re.findall('name="authenticity_token" value="(.*?)" />', res1.text)
    # print(token)


def

if __name__ == "__main__":
    login_V2()
