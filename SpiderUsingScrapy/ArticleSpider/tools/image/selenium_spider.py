from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
# 驱动路径
path = '/usr/bin/chromedriver'
# 创建浏览器对象
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

driver.get("https://www.zhihu.com/#signin")
t_selector = Selector(text=driver.page_source)
driver.find_element_by_css_selector(".view-signin input[name='account']").send_keys("13533401988")
driver.find_element_by_css_selector(".view-signin input[name='password']").send_keys("qazwsxedcrf123")
driver.find_element_by_css_selector(".view-signin button.sign-button").click()
# driver.quit()

