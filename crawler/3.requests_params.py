import requests

'''
3.2.1 在url携带参数
'''

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

url = "https://www.baidu.com?wd=python"

res = requests.get(url, headers=headers)
print(res.content.decode())
print(len(res.content.decode()))  # 364938

'''
3.2.2 通过params携带参数字典
'''

data = {
    "wd": "python"
}

# 带上请求参数发起请求，获取响应
res2 = requests.get(url, headers=headers, params=data)
print(res2.url)
