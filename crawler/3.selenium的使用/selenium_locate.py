
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
# 根据xpath获取元素对象，获取百度的搜索栏的输入框
driver.find_element_by_xpath('//*[@id="kw"]').send_keys("python")
# 通过css选择器进行元素定位
driver.find_element_by_css_selector("#kw").send_keys("python")
# 通过name属性进行元素定位
driver.find_element_by_name("wd").send_keys("python")
# 通过class属性进行元素定位
driver.find_element_by_class_name("s_ipt").send_keys("python")
# 获取百度点击click的图标栏 并发送点击的操作
driver.find_element_by_id("su").click()

# 通过link_text进行元素定位
driver.find_element_by_link_text("hao123").click()

# 通过link_text进行元素定位:部分链接文本
driver.find_element_by_partial_link_text("hao").click()

# 目标元素在当前html
driver.find_element_by_tag_name("title")



