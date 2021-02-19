from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
import random
url="https://tieba.baidu.com/p/7231141341"
# url="https://bbs.nga.cn/thread.php?stid=24955101"
options = webdriver.ChromeOptions()
# proxy = '127.0.0.1:10808'
# options.add_argument('--proxy-server=socks5://' + proxy)
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome
driver.get(url)

time.sleep(2.0)
content = driver.page_source.encode('utf-8')
soup = BeautifulSoup(content, 'html.parser')
print(soup)
# driver.quit()