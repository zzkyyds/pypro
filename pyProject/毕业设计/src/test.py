from Particle import Particle
from PSO import PSO
from util import dominates
import DataReader
import json
import main


def run():
    data = DataReader.readHumberger(
        'data\homberger_200_customer_instances\C2_2_7.TXT')
    scoreFunc = main.calScore

    pso = PSO(data['vehicleNum'], data['vehicleCapacity'],
              data['customers'], [1]*24, 20, 1000)
    pso.optimize(scoreFunc, dominates, 100,True,True)
    for x in pso.global_best:
        print(x.toInfo())

run()