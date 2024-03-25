import math
import itertools
from PSO import Particle





def calScore(vehicleRes: dict, departureTime: list, customers: list, roadCondition: list, maxSpeed: float):
    '''
    todo

    vehicleRes:车辆路径
    departureTime:车辆出发时间
    customers:顾客列表
    roadCondition:道路条件,拥堵程度 每小时拥堵程度

    return 计算得分=总成本,总满意度

    cost计算:时间车费（驾驶员工资，空调电费）+里程车费（油费）
    satisfy计算:满意度=顾客到达时间-顾客要求到达时间
    '''
    cost = 0.0
    satisfy = 0.0

    # 计算每个车辆的成本和满意度
    for k, v in vehicleRes.items():
        time = departureTime[k-1]
        nowPos = 0
        for i in itertools.chain(v, [0]):
            distance = math.sqrt((customers[i]['x']-customers[nowPos]['x'])**2+(
                customers[i]['y']-customers[nowPos]['y'])**2)
            time += distance/maxSpeed
            cost += distance
            if time < customers[i]['readyTime']:
                time = customers[i]['readyTime']
            if time > customers[i]['dueDate']:
                # cost += (time-customers[i]['dueDate'])
                satisfy += time-customers[i]['dueDate']
            time += customers[i]['serviceTime']

            nowPos = i

    return cost, satisfy
