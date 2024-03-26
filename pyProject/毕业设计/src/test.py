from Particle import Particle
from PSO import PSO
from util import dominates
import DataReader
import json
import main


def run():
    data = DataReader.readHumberger(
        'data\homberger_200_customer_instances\C2_2_8.TXT')
    scoreFunc = main.calScore

    pso = PSO(data['vehicleNum'], data['vehicleCapacity'], data['customers'],
              roadCondition=[1]*24, maxSpeed=60, particlesNum=250)
    pso.optimize(optimizeFunction=scoreFunc, dominateFunction=dominates,
                 iterations=1000, draw=True, adaptiveCoordinates=True)
    for x in pso.global_best:
        print(x.toInfo())



run()
