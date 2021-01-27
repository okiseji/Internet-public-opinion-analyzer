import requests
import bs4
import os
import re
import time
import urllib
import urllib.request
import random
from bs4 import BeautifulSoup
def get_html(url):
    try:
        # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        # kv={"usm":"3","rsv_idx":"2","rsv_page":"1"}
        r = requests.get(url, timeout=30)
        # proxies={'http':'36.248.132.13:9999'}
        # r = requests.get(url, timeout=30,proxies=proxies)
        r.raise_for_status()
        r.encoding = 'utf-8'
        # print(r.text)
        return r.text
    except:
        return " ERROR "
def get_content(url):
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('li', attrs={"class":['j_thread_list', 'clearfix']})
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find(
                'a', attrs={"class": ['j_th_tit']}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs={"class": ['j_th_tit']})['href']
            comment['name'] = li.find(
                'span', attrs={"class": ['tb_icon_author']}).text.strip()
            comment['time'] = li.find(
                'span', attrs={"class": ['pull-right is_show_create_time']}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={"class": ['threadlist_rep_num center_text']}).text.strip()
            comments.append(comment)
        except:
            print('出了点小问题')
    return comments
class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD= re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n  ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()
class BDTB(object):
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')
            return html
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                print ('连接百度贴吧失效，错误原因:', e.reason)
                return None
    def getTitle(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pat1, page)
        if result:
            print(result.group(1))
            return result.group(1)
        else:
            return None
    def getPageNum(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pat1, page)
        if result:
            return result.group(1)
        else:
            return None
    def getContent(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pat1, page)
        return self.tool.replace(items[0])
if __name__ == '__main__':
    base_url = 'http://tieba.baidu.com/f?kw=v&ie=utf-8'
    deep = 10
    url_list = []
    for p in range(0,deep):
        i=random.randint(0, 201)
        url_list.append(base_url + '&pn=' + str(50*i))
        print('now start!')
        for url in url_list:
            comments = get_content(url)
        print('No'+str(i)+"正在筛选")
        with open('定型文7.txt','a+',encoding='utf-8') as f:
            for comment in comments:
                baseURL = comment['link']
                bdtb = BDTB(baseURL,0)
                page_num = bdtb.getPageNum(1)
                print("a")
                if len(bdtb.getContent(1)) > 100:
                    bdtb.getTitle(1)
                    f.write("title:{}\n{}\n".format(bdtb.getTitle(1),bdtb.getContent(1)))
                else:
                    continue