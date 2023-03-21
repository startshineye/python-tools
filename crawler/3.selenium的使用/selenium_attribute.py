from selenium import webdriver

url = "http://www.baidu.com"
driver = webdriver.Chrome()
driver.get(url)

# 获取标签对象
w = driver.find_element_by_xpath('//*[@id="kw"]')
# 获取标签对象的文本跟属性
print(w.text, w.get_attribute("class"))

w.click() # 要求我们的标签支持点击
w.send_keys()  # 支持的是text input这类标签
w.clear()  # 对输入框做清空操作
