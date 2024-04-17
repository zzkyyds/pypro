from Particle import Particle
from PSO import PSO
from util import dominates
import DataReader
import json
import main
import drawer


def run():
    data = DataReader.readHumberger(
        'data\homberger_200_customer_instances\RC2_2_10 copy.TXT')
    scoreFunc = main.calScore

    pso = PSO(data['vehicleNum'], data['vehicleCapacity'], data['customers'],
              roadCondition=[1]*24, maxSpeed=30, particlesNum=300)
    pso.optimize(optimizeFunction=scoreFunc, dominateFunction=dominates,
                 iterations=500, draw=True, adaptiveCoordinates=True)
    res=pso.global_best[0]
    v=Particle.decode(res.position)
    drawer.drawTest(data['customers'],v,5)
    print(v)



run()
