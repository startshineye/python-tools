from selenium import webdriver
url = "https://bj.lianjia.com/"

driver = webdriver.Chrome()
driver.get(url)
js = "scrollTo(0,700)"
driver.execute_script(js)
el = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/p/a')
el.click()