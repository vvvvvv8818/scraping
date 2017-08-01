#coding=euc-kr
from bs4 import BeautifulSoup
import requests
import lxml
import datetime

def spider(url):
    src = requests.get(url)
    plain_text = src.text
    soup = BeautifulSoup(plain_text, 'lxml')    # use lxml parser

    res = soup.find_all('span', class_='spt_con up')

    soup = BeautifulSoup(str(res), 'lxml')
    res = soup.find_all('strong')
    return res


now = datetime.datetime.now()
print(now.strftime('[%Y-%m-%d / %H:%M:%S]'))

s = spider('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%ED%8C%8C%EC%9A%B4%EB%93%9C+%ED%99%98%EC%9C%A8')
s = str(s)
s = s.split('>')[1]
s = s.split('<')[0]
print ('lb : ' + s)

s = spider('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9C%A0%EB%A1%9C+%ED%99%98%EC%9C%A8')
s = str(s)
s = s.split('>')[1]
s = s.split('<')[0]
print ('euro : ' + s)
