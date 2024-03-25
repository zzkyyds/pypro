import math
import numpy as np
from drawer import drawXY



def readHumberger(file_path: str):
    res={}
    customers=[]
    res['customers']=customers
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if(line_number==1):
                res['caseName']=line.strip()
            elif(line_number==5):
                veh=line.split()
                res['vehicleNum']=int(veh[0])
                res['vehicleCapacity']=int(veh[1])
            elif(line_number>9):
                cust_no, xcoord, ycoord, demand, ready_time, due_date, service_time = map(int, line.split())
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



if __name__ == '__main__':
    res=readHumberger('data\homberger_200_customer_instances\C2_2_7.TXT')
    customers=res['customers']
    distance=np.array([math.sqrt((customers[i]['x']-customers[0]['x'])**2+(customers[i]['y']-customers[0]['y'])**2) for i in range(len(customers))])
    print(distance.mean())
    print(distance.std())
