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
            return(result.group(1))
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
        # i=4
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
    # bdtb.getTitle(1)
    page_num = bdtb.getPageNum(1)
    for i in range(page_num):
        # bdtb.getContent(i+1)
        strings += bdtb.getContent(i + 1)
        # print(strings)
    return strings
#统计工具类
#这段话提及了这些虚拟主播吗
def vtb(str):
    mention=set()
    vtbs={
    #国籍分类
    "国v":["国v","熊猫妹"],
    "日v":["日v","yhm","日本v","樱花妹"],
    #箱分类
    "asoul":["乐华","asoul","a烧","a骚","A烧","A骚","a-soul","A-soul","as","A-SOUL"],
    "p":["p家","巴黎"],
    "holo":["holo","猴楼","杏","木口","尸体","yagoo","YAGOO","cover","COVER","HOLO"],
    "nijisanji":["虹"],
    "vr":["vr","VR","微阿"],
    "monv": ["魔女"],
    #缝合人
    "meaqua":["meaqua","连体","六字母"],
    "七海": ["娜娜米", "nanami", "海子姐", "七海", "海皇","唯一指定","ybb"],

    #单个主播
    #asoul
    "diana": ["嘉", "然然", "洗脚婢"],
    "xiangwan": ["向晚", "顶碗", "晚晚", "晚指导"],
    "bella": ["贝拉", "北极星"],
    "carol": ["珈"],
    "nai0": ["乃琳", "乃0"],
    #hololive
    "gawr":["鲨"],
    "koko": ["tskk", "可可", "虫皇", "蝗", "龙皇", "憨憨龙", "会长", "尸体","coco","koko"],
    "lamy": ["菈米", "绿茶", "雪花","雪民","❄"],
    "aqua": ["夸", "圣皇", "aqua", "四字母", "阿库娅", "crew","あくあ"],
    "haato": ["赤井心", "哈恰玛", "haato", "心心"],
    "fubuki":["狐","fubuki","白上","坦克"],
    "pekora": ["兔", "pekora", "佩克拉","🐇","🐰","ぺこら"],
    "heitao": ["黑桃影", "桃皇", "♠", "大奈奈", "大莱莱","嘻嘻","薯条","🍟"],
    "doris":["朵子哥","朵莉丝","salute"],
    "robo":["萝卜"],
    "rusia":["粽","露西亚"],
    "matsuri":["祭","夏色"],
    "nene":["nene","桃铃"],
    #p家
    "mea": ["mea", "三字母", "财布", "神楽めあ", "天狗", "屑女人", "吊人", "天苟"],
    "serena": ["花园", "serena", "猫猫", "猫皇"],
    "ritsu":["律"],
    "pariy": ["帕里"],
    "oto": ["大姐", "oto", "老阿姨", "乙女音"],
    "erio": ["小红", "艾莉欧", "宦官", "幻官", "幻士", "赤"],
    #nijisanji&VR
    "alice": ["小兔子", "爱丽丝", "alice", "有栖"],
    "mito": ["月之美兔", "月ノ", "药水姐"],
    "geye": ["葛"],
    "chitose": ["千岁"],
    "azi": ["梓"],
    "aza": ["aza"],
    # 其他
    "hareru":["花丸","大嘴"],
    "kelala":["克拉拉"],
    "lili":["白银莉莉"],
    "tiantian":["天天"],
    "nyaru":["猫雷","小猫"],
    "zhanji":["战姬","歌姬"],
    "miemu":["咩姆"],
    "mieli":["咩栗"],
    "lulu":["lu","日记"],

    "nana":["狗妈","nana","辣辣","辛","七奈","奈奈","然妈","🐶🐴","🐶妈","🐶🐎","新冠","娜娜"],
    "haruka":["白神遥","豹豹"],
    "nanoha":["菜羽"],
    "sutera":["花宫"],
    "bt":["bt","冰糖","BT"],
    "hiiro":["hiiro","王牛奶"],
    "kitsuna":["老爱","爱酱","绊爱"],
    "yousa":["yousa","冷鸟"],
    "kyouha":["京华"],
    "beren":["贝伦","小贝","非常に"],
    "siiro":["小白"],
    "yui":["时雨"],
    "lanyin":["兰音"],
    "nanako":["菜菜子"],
    "sio":["汐","星宫","星宮"],
    "niki":["miki","奈姬"],
    "lunai":["鹿"],
    "hanser":["憨色","hanser"],
    "shanoa":["夏诺雅"],
    "sia":["小茜"],
    "chelsea":["切茜娅"],
    "sara":["星川"],
    "sanri":["三日","三拉夫"],
    }
    for p in vtbs.values():
        for q in p:
            if q in str:
                mention.add(list(vtbs.keys())[list(vtbs.values()).index(p)])
                break
    return mention
def add(mention,value,vtbs):
    for p in mention:
        if p not in vtbs:
            vtbs[p]=0
            vtbs[p]+=value
        else:
            vtbs[p] += value
    return vtbs
if __name__ == '__main__':

    vtbs={'yousa':1, 'mieli':1, 'kyouha':1, 'meaqua':1, 'aza':4, 'lili':2, 'monv':2,
    'nai0':2, 'hanser':3, 'miemu':77, 'lanyin':5, 'sara':5, 'sia':5, 'hiiro':6, 'ritsu':7,
    'pariy':8,'niki':10, 'hanser:':10, 'carol':11, 'matsuri':13, 'doris':14, 'chitose':15,
    'sio':16, 'gawr':17, 'zhanji':20, 'siiro':21, 'geye':24, 'lunai':26, 'kitsuna':31,
    'lulu':34, 'robo':37, 'vr':38, 'kelala':44, 'haato':44, 'hareru':49, 'nyaru':50, 'lamy':50, 'bt':76,
    'p':82, 'heitao':85, 'oto':99, 'fubuki':127, 'serena':132, 'xiangwan':141, '七海':158, '日v':166, '国v':188,
    'pekora':188, 'alice':204, 'yui':204, 'erio':212, 'nijisanji':225, 'tiantian':250, 'nana':257, 'azi':306,
    'koko':380, 'beren':415, 'mea':590, 'asoul':604, 'bella':677, 'holo':816, 'aqua':821, 'diana':875}
    tiebaurl = 'http://tieba.baidu.com/f?kw=v&ie=utf-8'
    yemianurl=pagelist(1,tiebaurl)
    yemianurllist= urllist(yemianurl)
    for i in range(0,50):
        tieziurl=yemianurllist[i]
        # tielist(tieziurl)
        tieinfo=tielist(tieziurl)
        bdtb = BDTB(tieziurl, 0)
        theme=str(bdtb.getTitle(1) + tieinfo[0])
        if vtb(theme):
            vtbs=add(vtb(theme),len(tieinfo),vtbs)
            for tie in tieinfo:
                vtbs=add(vtb(tie),1,vtbs)
        else:
            for tie in tieinfo:
                vtbs=add(vtb(tie),1,vtbs)
        print(vtbs)
    #     # print("请等待10sec")
    #     # time.sleep(10.0)
    print(sorted(vtbs.items(), key=lambda d: d[1]))







