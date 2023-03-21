from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# options.set_headles() # 无界面模式的另外一种开启方式
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://www.baidu.com")
driver.save_screenshot("no_header_browser.png")
driver.quit()
