from Particle import Particle
from PSO import PSO
from util import dominates
import DataReader
import json
import main
import drawer


def run():
    # 'data\homberger_200_customer_instances\RC2_2_10 copy.TXT'
    # 'data\homberger_200_customer_instances\RC2_2_9.TXT'
    data = DataReader.readHumberger(
        'data\homberger_200_customer_instances\RC2_2_10 copy.TXT')
    scoreFunc = main.calScore

    pso = PSO(data['vehicleNum'], data['vehicleCapacity'], data['customers'],
              roadCondition=[1]*24, maxSpeed=30, particlesNum=300)
    pso.optimize(optimizeFunction=scoreFunc, dominateFunction=dominates,
                 iterations=1000, draw=True, adaptiveCoordinates=True,kopt=5,kCount=30)
    res=pso.kopt
    res.sort(key=lambda x:x.cost)
    # res.sort(key=lambda x:x.cost)
    # res=res[len(res)//2]
    res=res[0]
    v=Particle.decode(res.position)
    drawer.drawTest(data['customers'],v,4)
    print(res.toInfo())



if __name__=='__main__':
    run()
