from __future__ import with_statement
from __future__ import absolute_import
import requests
import bs4
import os
import re
import time
import urllib
import urllib2, urllib
from bs4 import BeautifulSoup
from io import open
def get_html(url):
    try:
        # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        # kv={"usm":"3","rsv_idx":"2","rsv_page":"1"}
        # r = requests.get(url, timeout=30, headers=headers)
        proxies={u'http':u'http://120.83.108.195:9999'}
        r = requests.get(url, timeout=30,proxies=proxies)
        r.raise_for_status()
        r.encoding = u'utf-8'
        # print(r.text)
        return r.text
    except:
        return u" ERROR "
def get_content(url):
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html, u'lxml')
    liTags = soup.find_all(u'li', attrs={u"class":[u'j_thread_list', u'clearfix']})
    for li in liTags:
        comment = {}
        try:
            comment[u'title'] = li.find(
                u'a', attrs={u"class": [u'j_th_tit']}).text.strip()
            comment[u'link'] = u"http://tieba.baidu.com/" + li.find(u'a', attrs={u"class": [u'j_th_tit']})[u'href']
            comment[u'name'] = li.find(
                u'span', attrs={u"class": [u'tb_icon_author']}).text.strip()
            comment[u'time'] = li.find(
                u'span', attrs={u"class": [u'pull-right is_show_create_time']}).text.strip()
            comment[u'replyNum'] = li.find(
                u'span', attrs={u"class": [u'threadlist_rep_num center_text']}).text.strip()
            comments.append(comment)
        except:
            print u'出了点小问题'
    return comments
class Tool(object):
    removeImg = re.compile(u'<img.*?>| {7}|')
    removeAddr = re.compile(u'<a.*?>|</a>')
    replaceLine = re.compile(u'<tr>|<div>|</div>|</p>')
    replaceTD= re.compile(u'<td>')
    replacePara = re.compile(u'<p.*?>')
    replaceBR = re.compile(u'<br><br>|<br>')
    removeExtraTag = re.compile(u'<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,u"",x)
        x = re.sub(self.removeAddr,u"",x)
        x = re.sub(self.replaceLine,u"\n",x)
        x = re.sub(self.replaceTD,u"\t",x)
        x = re.sub(self.replacePara,u"\n  ",x)
        x = re.sub(self.replaceBR,u"\n",x)
        x = re.sub(self.removeExtraTag,u"",x)
        return x.strip()
class BDTB(object):
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = u'?see_lz=' + unicode(seeLZ)
        self.tool = Tool()
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + u'&pn=' + unicode(pageNum)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            html = response.read().decode(u'utf-8')
            return html
        except urllib2.URLError, e:
            if hasattr(e, u'reason'):
                print u'连接百度贴吧失效，错误原因:', e.reason
                return None
    def getTitle(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(ur'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pat1, page)
        if result:
            print result.group(1)
            return result.group(1)
        else:
            return None
    def getPageNum(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(ur'<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pat1, page)
        if result:
            return result.group(1)
        else:
            return None
    def getContent(self, pageNum):
        page = self.getPage(pageNum)
        pat1 = re.compile(ur'<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pat1, page)
        return self.tool.replace(items[0])
if __name__ == u'__main__':
    base_url = u'http://tieba.baidu.com/f?kw=v&ie=utf-8'
    deep = 2
    url_list = []
    for i in xrange(0, deep):
        url_list.append(base_url + u'&pn=' + unicode(50
                                                * i))
        print u'now start!'
        for url in url_list:
            comments = get_content(url)
        print u'No'+unicode(i)+u"正在筛选"
        with open(u'定型文4.txt',u'a+',encoding=u'utf-8') as f:
            for comment in comments:
                baseURL = comment[u'link']
                bdtb = BDTB(baseURL,0)
                page_num = bdtb.getPageNum(1)
                print u"a"
                if len(bdtb.getContent(1)) > 50:
                    bdtb.getTitle(1)
                    f.write(u"title:{}\n{}\n".format(bdtb.getTitle(1),bdtb.getContent(1)))
                else:
                    continue