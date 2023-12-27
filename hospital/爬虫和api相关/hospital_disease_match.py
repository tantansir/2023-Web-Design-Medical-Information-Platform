# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 20:06:13 2023

@author: wangj
"""

import pandas as pd


d1=pd.read_excel(r"C:\Users\wangj\Desktop\web开发-hospital\department.xlsx")
t1=d1.to_dict('index')

for i in range(32):
    if "暂无" in t1[i]['对应疾病']:
        kname=t1[i]['科室名称']
        print(kname,i)
        
        
d2=pd.read_excel(r"C:\Users\wangj\Desktop\web开发-hospital\hospital_info.xlsx")
t2=d2.to_dict('index')
for j in range(45):
    if kname==t2[j]['优势科室1'] or kname==t2[j]['优势科室2'] or kname==t2[j]['优势科室3']:
        hname=t2[j]['医院名称']
        print(hname,j)