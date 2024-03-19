import numpy as np
import pandas as pd



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



print(readHumberger('data\homberger_200_customer_instances\RC2_2_10.TXT'))