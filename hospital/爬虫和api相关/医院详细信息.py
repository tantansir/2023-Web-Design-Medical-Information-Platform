# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 17:24:35 2023

@author: wangj
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas

url1 = "https://www.haodf.com/hospital/471/jieshao.html"
url2 = "https://www.haodf.com/hospital/469/jieshao.html"
url3 = "https://www.haodf.com/hospital/474/jieshao.html"
url4 = "https://www.haodf.com/hospital/425/jieshao.html"
url5 = "https://www.haodf.com/hospital/430/jieshao.html"
url6 = "https://www.haodf.com/hospital/1157/jieshao.html"
url7 = "https://www.haodf.com/hospital/6972309857/jieshao.html"
url8 = "https://www.haodf.com/hospital/424/jieshao.html"
url9 = "https://www.haodf.com/hospital/422/jieshao.html"
url10 = "https://www.haodf.com/hospital/428/jieshao.html"
url11 = "https://www.haodf.com/hospital/416/jieshao.html"
url12 = "https://www.haodf.com/hospital/473/jieshao.html"
url13 = "https://www.haodf.com/hospital/418/jieshao.html"
url14 = "https://www.haodf.com/hospital/429/jieshao.html"
url15 = "https://www.haodf.com/hospital/829/jieshao.html"
url16 = "https://www.haodf.com/hospital/826/jieshao.html"
url17 = "https://www.haodf.com/hospital/818/jieshao.html"
url18 = "https://www.haodf.com/hospital/420/jieshao.html"
url19 = "https://www.haodf.com/hospital/423/jieshao.html"
url20 = "https://www.haodf.com/hospital/468/jieshao.html"
url21 = "https://www.haodf.com/hospital/476/jieshao.html"
url22 = "https://www.haodf.com/hospital/419/jieshao.html"
url23 = "https://www.haodf.com/hospital/466/jieshao.html"
url24 = "https://www.haodf.com/hospital/827/jieshao.html"
url25 = "https://www.haodf.com/hospital/831/jieshao.html"
url26 = "https://www.haodf.com/hospital/421/jieshao.html"
url27 = "https://www.haodf.com/hospital/5664349110/jieshao.html"
url28 = "https://www.haodf.com/hospital/1064/jieshao.html"
url29 = "https://www.haodf.com/hospital/6522928020/jieshao.html"
url30 = "https://www.haodf.com/hospital/1056/jieshao.html"
url31 = "https://www.haodf.com/hospital/467/jieshao.html"
url32 = "https://www.haodf.com/hospital/1938/jieshao.html"
url33 = "https://www.haodf.com/hospital/991/jieshao.html"
url34 = "https://www.haodf.com/hospital/1196/jieshao.html"
url35 = "https://www.haodf.com/hospital/431/jieshao.html"
url36 = "https://www.haodf.com/hospital/823/jieshao.html"
url37 = "https://www.haodf.com/hospital/143453618/jieshao.html"
url38 = "https://www.haodf.com/hospital/426/jieshao.html"
url39 = "https://www.haodf.com/hospital/427/jieshao.html"
url40 = "https://www.haodf.com/hospital/440/jieshao.html"
url41 = "https://www.haodf.com/hospital/433/jieshao.html"
url42 = "https://www.haodf.com/hospital/434/jieshao.html"
url43 = "https://www.haodf.com/hospital/432/jieshao.html"
url44 = "https://www.haodf.com/hospital/6972279831/jieshao.html"
url45 = "https://www.haodf.com/hospital/417/jieshao.html"

hospital_url_list=[url1,url2,url3,url4,url5,url6,url7,url8,url9,url10,url11,url12,url13,url14,url15,url16,url17,url18,url19,url20,url21,url22,url23,url24,url25,url26,url27,url28,url29,url30,url31,url32,url33,url34,url35,url36,url37,url38,url39,url40,url41,url42,url43,url44,url45]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'} 

names=[];phones=[];addresses=[];intrs=[]
for url in hospital_url_list:  
    response = requests.get(url1,headers=headers)
    content = response.text
    
    
    soup = BeautifulSoup(content, "html.parser")
       
    attrs0={"class":"i-other"}
    name = soup.find("h1", attrs=attrs0)
    attrs1={"class":"j-p-item"}
    phone = soup.find("div", attrs=attrs1)
    attrs2={"class":"j-i-cont"}
    address=soup.find("p",attrs=attrs2)
    attrs3={"class":"h-j-info"}
    intr=soup.find("div",attrs=attrs3)
    
    names.append(name.string)
    phones.append(phone.string)
    addresses.append(address.string)
    intrs.append(intr.string)

    print();print();
    
print(names); print(phones); print(addresses); print(intrs);   
