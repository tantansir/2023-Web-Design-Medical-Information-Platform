# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 15:58:01 2023

@author: wangj
"""


import requests
import socket

key = '1ae93e79c00d18361431fb9e1b254dfd'


# 获取本地主机的真实IP
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

    
if __name__ == '__main__':
    print(get_ip())


def iploc(ip:str):

    parameters = {'key':key,'ip':ip,'output':'json'}
    r = requests.get('https://restapi.amap.com/v3/ip?parameters',params = parameters)
    data = r.json()
    return data


print(iploc())
