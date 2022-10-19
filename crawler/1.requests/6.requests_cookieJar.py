import requests
import requests.utils

url = "https://www.baidu.com"
res = requests.get(url)

# cookieJar对象
print(res.cookies)

# cookieJar对象转换成cookies对象
cookies_dict = requests.utils.dict_from_cookiejar(res.cookies)
print(cookies_dict)

# cookies对象转换成cookieJar
cookieJar = requests.utils.cookiejar_from_dict(cookies_dict)
print(cookieJar)
