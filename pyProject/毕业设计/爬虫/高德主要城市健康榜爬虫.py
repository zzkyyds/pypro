from datetime import datetime
import requests

def parseTime(time):
    time=time/1000
    return datetime.fromtimestamp(time)

def getCityMap():
    cityUrl='https://report.amap.com/ajax/getCityInfo.do?'
    response = requests.get(cityUrl)
    data = response.json()
    map={i['code']:i['name'] for i in data}
    return map


def getCityTrafficCongestionDelayIndex(cityCode):
    '''
    返回= [time,拥堵延时指数]的lis,size=24
    '''
    url='https://report.amap.com/ajax/cityHourly.do?cityCode={}&dataType=1'.format(cityCode)
    response = requests.get(url)
    data = response.json()
    for i in data:
        i[0]=parseTime(i[0])
    return data

def getCityHighDelayProportion(cityCode):
    url='https://report.amap.com/ajax/cityHourly.do?cityCode={}&dataType=2'.format(cityCode)
    response = requests.get(url)
    data = response.json()
    for i in data:
        i[0]=parseTime(i[0])
    return data
