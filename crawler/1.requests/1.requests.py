import requests

url = 'https://www.baidu.com'
response = requests.get(url)

# 第一种模式
print(response.encoding)
response.encoding = 'utf8'
print(response.text)
print(response.encoding)

# 第二种模式

# response.content存储的是bytes的响应源码
print(response.content)

print(response.content.decode())
