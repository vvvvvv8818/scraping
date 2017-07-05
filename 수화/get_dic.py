#coding: euc-kr
from bs4 import BeautifulSoup
import requests
from __builtin__ import str
 
 
class OriginNo:
    def __init__(self):
        self.sess = requests.session()
    def getOriginNo(self):
        url='http://sldict.korean.go.kr/front/sign/signList.do'
        for pagenum in range(1, 1296+1):
            ret = []
            payload = {'pageIndex':pagenum, 'top_category':'CTE'}
            
            req = self.sess.post(url, payload)
            if req.status_code == 400:
                return None
    #         response = requests.get(url)
    #         html_content = response.text.encode(response.encoding)
            
            bs = BeautifulSoup(req.text, "html.parser")
            all = bs.find_all('a', class_='hand_thumb')
            i = 0
            for a in all:
                href = a['href']
                str = href.split("'")
                ret.append(str[1])
                i += 1
           
        return ret
 
 
class Handman:
    def __init__(self):
        self.sess = requests.session()
    def getData(self, uid):
        wrap = {}
        url = 'http://sldict.korean.go.kr/front/sign/signContentsView.do'
        payload = {"origin_no":uid, "top_category":"CTE"}
        
        req = self.sess.post(url, payload)
        if req.status_code == 400:
            return None
        bs = BeautifulSoup(req.text, "html.parser")
        data = bs.find("dl")
        if data is None:
            return None
        dds = data.findAll("dd")
        wrap['description'] = dds[1].text
#         wrap['origin_language'] = dds[2].text
 
        data = bs.find_all('dl', class_='content_view_dis')[1]
        
        dds2 = data.findAll('dd')
        wrap['word'] = "".join(dds2[0].text.split())
        wrap['mean'] = dds2[1].text
        
        
        
        payload = {"origin_no":uid, "category":"CTE017", "size":"high", "viewSelect":"high"}
        req = self.sess.post("http://sldict.korean.go.kr/front/sign/include/controlVideoSpeed.do",payload)
        del bs
        bs = BeautifulSoup(req.text, "html.parser")
        video = bs.find("video")
        wrap['video_link'] = video.find("source", attrs={"type":"video/mp4"}, src=True)['src']
        return wrap
    
    def getInfo(self, uid):
        data = self.getData(uid)
        if data is None:
            return None
        ret = u""
        ret += u"설명 : %s\n영상 링크 : %s\n단어 : %s\n뜻 : %s\n" % (data['description'], data['video_link'], data['word'], data['mean'])
        return ret 
 
 
 
hand = Handman()
originNo = OriginNo()
 
numbers = originNo.getOriginNo()
print numbers
 
for number in numbers:
    print number
    data = hand.getInfo(number)
    if data is None:
        print "존재하지 않습니다"
    else:
        print data