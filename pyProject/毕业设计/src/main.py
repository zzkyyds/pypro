import math
from PSO import Particle


def dominates(a: Particle, b: Particle):
    '''
    比较两个个体的支配关系
    '''
    if a.cost < b.cost and a.satisfy > b.satisfy:
        return 1
    if a.cost > b.cost and a.satisfy < b.satisfy:
        return -1
    return 0


def calScore(vehicleRes: dict, departureTime: list, customers: list, roadCondition: list, maxSpeed: float):
    '''
    todo

    vehicleRes:车辆路径
    departureTime:车辆出发时间
    customers:顾客列表
    roadCondition:道路条件,拥堵程度 每小时拥堵程度

    return 计算得分=总成本,总满意度

    cost计算:时间车费（驾驶员工资，空调电费）+里程车费（油费）
    '''
    cost = 0.0
    satisfy = 0.0

    # 计算每个车辆的成本和满意度
    for k, v in vehicleRes.items():
        time = departureTime[k]
        nowPos = 0
        for i in v:
            time += math.sqrt((customers[i]['x']-customers[nowPos]['x'])**2+(
                customers[i]['y']-customers[nowPos]['y'])**2)/maxSpeed
            if time < customers[i]['readyTime']:
                time = customers[i]['readyTime']
            if time > customers[i]['dueDate']:
                cost += (time-customers[i]['dueDate'])
            time += customers[i]['serviceTime']


            nowPos = i

    return cost, satisfy
