from datetime import datetime
import requests
import json
import os

def parseTime(time):
    time=time/1000
    return datetime.fromtimestamp(time)

def getCityMap():
    '''
    返回= {cityCode:cityName}的map
    '''
    cityUrl='https://report.amap.com/ajax/getCityInfo.do?'
    response = requests.get(cityUrl)
    data = response.json()
    map={i['code']:i['name'] for i in data}
    return map


def getCityTrafficCongestionDelayIndex(cityCode):
    '''
    返回= [time,拥堵延时指数]的list,size=24
    '''
    url='https://report.amap.com/ajax/cityHourly.do?cityCode={}&dataType=1'.format(cityCode)
    response = requests.get(url)
    data = response.json()
    return data

def getCityHighDelayProportion(cityCode):
    '''
    返回= [time,高延时比例]的list,size=24
    '''
    url='https://report.amap.com/ajax/cityHourly.do?cityCode={}&dataType=2'.format(cityCode)
    response = requests.get(url)
    data = response.json()
    return data

def spider():
    cityMap=getCityMap()
    res={}
    delayIndex={}
    highDelayProportion={}
    res['delayIndex']=delayIndex
    res['highDelayProportion']=highDelayProportion

    for cityCode in cityMap:
        delayIndex[cityMap[cityCode]]=getCityTrafficCongestionDelayIndex(cityCode)
        highDelayProportion[cityMap[cityCode]]=getCityHighDelayProportion(cityCode)
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    directory = 'data/拥堵数据'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f'{current_date}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)

def read():
    current_date = datetime.now().strftime('%Y-%m-%d')
    directory = 'data/拥堵数据'
    filename = os.path.join(directory, f'{current_date}.json')
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)


if __name__ == '__main__':
    spider()
