from selenium import webdriver

# 指定driver的绝对路径
driver = webdriver.PhantomJS(executable_path='/Users/xiexinming/software/phantomjs-2.1.1-macosx/bin/phantomjs')
# driver = webdriver.Chrome(executable_path='/home/worker/Desktop/driver/chromedriver')

# 向一个url发起请求
driver.get("http://www.itcast.cn/")

# 把网页保存为图片
driver.save_screenshot("itcast.png")

# 退出模拟浏览器
driver.quit() # 一定要退出！不退出会有残留进程！