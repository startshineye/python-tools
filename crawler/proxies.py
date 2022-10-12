import requests

url = "https://www.baidu.com"
#response = requests.get(url)

proxies = {
    "http": "http://120.194.55.139:6969",
   # "https": "https://120.194.55.139:6969"
}

response = requests.get(url, proxies=proxies, timeout=10)
print(response.text)
