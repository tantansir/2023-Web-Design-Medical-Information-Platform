import requests
from geopy.distance import geodesic
 
 
KEY = '1ae93e79c00d18361431fb9e1b254dfd'
 

def stt(s1):
     
    lst=s1.split(',')
    lst[0],lst[1]=lst[1],lst[0]
    t1=tuple(lst)
    return t1


def geocode(address):
    """
    根据地名，获取经纬度
    """
    parameters = {'address': address, 'key': KEY}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    # print(answer)
    # print(type(answer))
    # print(address + "的经纬度：", answer['geocodes'][0]['location'])
    return answer['geocodes'][0]['location']
