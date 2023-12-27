# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 21:02:55 2023

@author: wangj
"""

import pandas as pd
import re

fp=open(r"C:\Users\wangj\Desktop\web开发-hospital\department.txt",'r',encoding='utf-8')


t1=fp.readlines()
d1=[];d2=[]
for i in range(len(t1)):
    if i%2==0: 
        d1.append(re.sub('\n',"",t1[i]))
    else:
        d2.append(re.sub("\t",",",t1[i]))

data={"科室名称":d1,"对应疾病":d2}
df=pd.DataFrame(data)
df.to_excel(r"C:\Users\wangj\Desktop\web开发-hospital\department.xlsx",index=False)
fp.close()