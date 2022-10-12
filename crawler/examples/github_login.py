'''
模拟github的数据登录;因为是会连续发送多次请求进行数据爬取，所以，我们需要使用requests的session
'''

import requests
import re
import time


def login():
    # session
    session = requests.session()
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    # url1-获取token
    url1 = "https://github.com/login"
    # 发送请求获取响应
    res1 = session.get(url1, headers=headers)
    print(res1.text)
    # 正则获取token里面的值
    token = re.findall('name="authenticity_token" value="(.*?)" />', res1.text)
    print(token)

    # url2-登录
    url2 = "https://github.com/session"
    # 构建表单数据
    tm = int(round(time.time() * 1000))
    data = {
        "commit": "Sign in",
        "authenticity_token": token,
        "login": "startshineye",
        "password": "xxxxx",
        "webauthn-support": "supported",
        "webauthn-iuvpaa-support": "supported",
        "return_to": "https://github.com/login",
        "allow_signup": "",
        "client_id": "",
        "integration": "",
        "required_field_e9c5": "",
        "timestamp": tm
    }
    # 发送请求登录
    res2 = session.post(url2, headers=headers, data=data)


    # url3-验证
    res3 = session.get("https://github.com/startshineye", headers=headers)
    print(res3.text)


if __name__ == "__main__":
    login()
