# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 14:11:05 2023

@author: wangj
"""

import requests
from bs4 import BeautifulSoup
import re

url = "https://www.haodf.com/hospital/list-31.html"
key="三甲"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'} 

response = requests.get(url,headers=headers)
content = response.text

soup = BeautifulSoup(content, "html.parser")
   
attrs1={"class":"m_ctt_green"}
hospital_list = soup.find_all("div", attrs=attrs1)


for hospital in hospital_list:
    names = hospital.find_all("li")
    for name in names:
        character=name.find("span")

        if key in character.string:
            #print(character.string)
            n1=re.match(r"(\s.*\s?)",name.text).group(1)
            print("医院名称:", n1)               
            print("特点:", character.string.strip())  
                
            print()
            
            
            
