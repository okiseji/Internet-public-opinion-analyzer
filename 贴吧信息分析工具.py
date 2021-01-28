import requests
import bs4
import os
import re
import time
import urllib
import urllib.request
import random
from bs4 import BeautifulSoup
#洗洁精类
class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD= re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    #洗洁精
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n  ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()
#帖子获取信息类
class BDTB(object):
    #seeLZ: 0:查看所有回复 1:只看楼主回复
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
    #获取帖子页面数内容
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            #print response.read()
            html = response.read().decode('utf-8')
            # print(html)
            return html
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                print ('连接百度贴吧失效，错误原因:', e.reason)
                return None
    #获取帖子标题
    def getTitle(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pat1, page)
        if result:
            #打印title
            print("title:"+result.group(1))
        else:
            return None
    #获取帖子回复页数
    def getPageNum(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pat1, page)
        if result:
            # print(result.group(1))
            return int(result.group(1))
        else:
            return None
    #获取帖子回复内容
    def getContent(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(r'<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pat1, page)
        stringc = []
        # for item in items:
        #     print (item)
        floor = 1
        for item in items:
            # print("")
            # print('第%s页的帖子内容:' %pageNum)
            # print(floor,u'楼')
            # 打印回复贴的内容
            # print(self.tool.replace(item))
            stringc.append(self.tool.replace(item))
            floor += 1
        return stringc
#贴吧主页获取
#网址爬虫框架
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
#得到帖子的各项数据
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
#创造工具函数
#创造贴吧每页链接
def pagelist(num,base_url):
    url_list = []
    for p in range(0, num):
        i = random.randint(0, 201)
        url_list.append(base_url + '&pn=' + str(50 * i))
        print('No' + str(i) + "正在筛选")
        print(url_list)
    return url_list
#创造贴吧每页帖子的链接
def urllist(url_list):
    baseURL_list=[]
    for url in url_list:
        comments = get_content(url)
        for comment in comments:
            baseURL = comment['link']
            baseURL_list.append(baseURL)
    print(baseURL_list)
    return baseURL_list
#创造帖子回复信息
def tielist(url):
    strings = []
    baseURL=url
    bdtb = BDTB(baseURL,0)
    bdtb.getTitle(1)
    page_num = bdtb.getPageNum(1)
    for i in range(page_num):
        # bdtb.getContent(i+1)
        strings += bdtb.getContent(i + 1)
        print(strings)
    return strings
#统计工具类
#还没写