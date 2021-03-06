import requests,time
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo

url='https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',
    'Referer':'http://www.baidu.com'
    }


client = pymongo.MongoClient('80.80.1.80',27017)
db_spider = client['spider']
page_douban = db_spider['douban']


def get_page(url):
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
#            res.encoding='utf-8'
            return res.text
    except RequestException:
        return None

def parse_index_page(html):
    soup = BeautifulSoup(html,'lxml')
    tbs = soup.select("#content > div > div.article > div:nth-of-type(2) > div > table > tbody > tr > td")
    for tb in tbs:
        page_douban.insert_one({'page' : tb.get_text(),'link' : tb.a.get('href')})
        print("Get down page"+tb.get_text())    
#    return data     
 
def main():
    html = get_page(url)
    parse_index_page(html)

if __name__=="__main__":
    main()