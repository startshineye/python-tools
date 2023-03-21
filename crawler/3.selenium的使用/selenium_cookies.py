from selenium import webdriver
driver = webdriver.Chrome()
url = "http://www.baidu.com"
driver.get(url)
print(driver.get_cookies())


# 将我们的driver获取的cookies转换成我们的字典
cookies = {}
'''
for data in driver.get_cookies():
    print(data)
    cookies[data['name']] = data['value']
'''
# 上面转换成：字典推导式/列表推导式
cookies = {data['name']: data['value'] for data in driver.get_cookies()}

print(cookies)