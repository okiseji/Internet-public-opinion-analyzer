from bs4 import BeautifulSoup
# import urllib2
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# board = input('board:')
# pages = int(input('pages:'))
board="vt"
pages=1
imgsize = 150
baseurl = "http://boards.4chan.org/"+board+"/"
proxies = {
    'http'  : 'socks5://127.0.0.1:10808',
    'https' : 'socks5://127.0.0.1:10808'
}
f = open('./4chan2.txt','w',encoding='utf=8')
# loadedimg = []
# bigimg = []
s = requests.Session()

def getimg(str):
    page = s.get(str)
    soup = BeautifulSoup(page.text, 'html.parser')
    imgs = soup.find_all('a', attrs={"class": "fileThumb"})
    for img in imgs:
        url = "https:" + img.find('img').get('src')
        # print(url)
        options = webdriver.ChromeOptions()
        proxy = '127.0.0.1:10808'
        options.add_argument('--proxy-server=socks5://' + proxy)
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.google.com/imghp')
        driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[3]/div[2]/span').click()
        driver.find_element_by_xpath('//*[@id="Ycyxxc"]').send_keys(url)
        driver.find_element_by_xpath('//*[@id="RZJ9Ub"]').click()
        text = driver.find_element_by_xpath('//*[@id="topstuff"]/div/div[2]/a').text
        print(text)
        driver.quit()
    return "picture:"+text
# getimg("https://boards.4channel.org/vt/thread/173177/havent-watched-a-single-watame-stream")
for page in range(1,pages+1):
    print(page)
    if(page>1):
        pageurl = baseurl + str(page) +"/"
    else:
        pageurl = baseurl
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
 #   req = urllib2.Request(pageurl, headers=hdr)         # 请求头，或许可以改成requests库内版本
#    response = requests(pageurl, headers=hdr).text
    html_doc = s.get(pageurl, headers=hdr, proxies=proxies).text        # response.text()
    soup = BeautifulSoup(html_doc, 'html.parser')
    subsoups = []
    replylinks = soup.find_all('a',attrs={'class':"replylink"},text="Reply")    # 找到所有形如<a class="replyLink" ...>Reply</a>的标签
    # 我大概明白这里的逻辑了，我找了一下原网页，reply的按钮只会有这个帖子对应的那些东西（就是类似于，一个贴吧的一个帖子），然后你就可以只抓取这个帖子了
    for link in replylinks:
        print(str(baseurl+link.get('href')))
        f.write(str(baseurl+link.get('href')))
        req = s.get(str(baseurl+link.get('href')), headers=hdr,proxies=proxies)  # 请求每个reply到的链接
        subsoup = BeautifulSoup(req.text,'html.parser')#存下结构化之后的reply的链接
        getimg(str(baseurl + link.get('href')))
        for atag in subsoup.find_all('a'):
            atag.decompose()
        for message in subsoup.find_all('blockquote'):
            f.write('\n' + message['id'][1:] + '\n' + message.get_text(separator="\n"))
