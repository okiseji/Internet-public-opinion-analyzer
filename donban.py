from bs4 import BeautifulSoup
import requests
headers = {'User-Agent': 'Mozilla/5.0'}
r=requests.get("https://www.douban.com/group/asoul/",headers=headers)
print(r.status_code)
soup=BeautifulSoup(r.text,"html.parser")
a=soup.find_all("td",attrs={"class":"title"})
for i in a:
    print(i)