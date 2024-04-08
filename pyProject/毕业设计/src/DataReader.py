import math
from matplotlib import pyplot as plt
import numpy as np
from drawer import drawXY


def readHumberger(file_path: str):
    res = {}
    customers = []
    res['customers'] = customers
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if (line_number == 1):
                res['caseName'] = line.strip()
            elif (line_number == 5):
                veh = line.split()
                res['vehicleNum'] = int(veh[0])
                res['vehicleCapacity'] = int(veh[1])
            elif (line_number > 9):
                cust_no, xcoord, ycoord, demand, ready_time, due_date, service_time = map(
                    int, line.split())
                customer = {
                    'cusNo': cust_no,
                    'x': xcoord,
                    'y': ycoord,
                    'demand': demand,
                    'readyTime': ready_time,
                    'dueDate': due_date,
                    'serviceTime': service_time
                }
                customers.append(customer)

    return res


def drawMap(customers: list):
    '''
    绘制客户分布图
    '''
    x = [e.get('x') for e in customers]
    y = [e.get('y') for e in customers]
    first_x = x[0]
    first_y = y[0]

    plt.scatter(first_x, first_y, color='red')
    plt.scatter(x[1:], y[1:], color='#66ccff')
    plt.show()


if __name__ == '__main__':
    res = readHumberger('data\homberger_200_customer_instances\C2_2_7.TXT')
    customers = res['customers']
    drawMap(customers)
