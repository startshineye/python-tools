import time
from selenium import webdriver

# 通过指定chromedriver的路径来实例化driver对象，chromedriver放在当前目录。
# driver = webdriver.Chrome(executable_path='./chromedriver')
# chromedriver已经添加环境变量
driver = webdriver.Chrome()
# 控制浏览器访问url地址
driver.get("https://www.baidu.com/")

# 在百度搜索框中搜索'python'
# 我们通过元素定位，定位到我们需要在baidu浏览器里面需要输入的字体：driver.find_element_by_id('kw')
# 然后在浏览器中输入:python；send_keys('python')
driver.find_element_by_id('kw').send_keys('python')
# 点击'百度搜索'
# 定位到su的点击按钮。然后执行点击操作：click()
driver.find_element_by_id('su').click()

time.sleep(6)
# 退出浏览器
driver.quit()
