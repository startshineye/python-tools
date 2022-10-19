import requests

url = 'https://www.baidu.com'
response = requests.get(url)

# 第一种模式
print(len(response.content.decode()))
print(response.content.decode())

print(response.request.headers)
# 构建请求头字典
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

# 发送请求
res = requests.get(url, headers=headers)
print(res.content.decode())
print(len(res.content.decode()))
