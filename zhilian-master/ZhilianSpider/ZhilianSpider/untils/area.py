import urllib.request as ur
from bs4 import BeautifulSoup as bs
import pymongo
client = pymongo.MongoClient(host='127.0.0.1',port=27017)
# client.admin.authenticate("", "")
zhilian = client['area']
Zhilian_area = zhilian["Zhilian_area"]

def getreq(url):
    header={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Cookie':'guid = c17c - 320b - c059 - f9b1;key = c4746acf0aa8c8a139fae3a1a47fc9a0'
    }

    req = ur.Request(url,headers=header)
    html = ur.urlopen(req).read().decode('utf-8')
    return html


def getarea(html):
    soup = bs(html, 'html.parser')
    if soup.select('.infor div dl dd a strong'):
        item = soup.select('.infor div dl dd a strong')
        for i in item:
            a = i.get_text()
            data = {'area': a}
            print(data)
            Zhilian_area.insert(data)



if __name__ == "__main__":
    url = "https://www.zhaopin.com/citymap.html"
    html = getreq(url)
    getarea(html)





