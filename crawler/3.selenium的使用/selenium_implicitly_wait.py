from selenium import webdriver

url = "http://www.baidu.com"

driver = webdriver.Chrome()
driver.get(url)

driver.implicitly_wait(5)

el = driver.find_element_by_xpath('//*[@id="s_lg_img_aging11"]')
print(el)
