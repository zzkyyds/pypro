import Particle
import FastNondominatedSort

class PSO:
    def __init__(self, vehicleNum: int, capacity: int, customers: list[dict], roadCondition: list, maxSpeed: float,
                 particlesNum: int):
        '''
        vehicleNum:车辆数
        capacity:车辆容量
        customers:顾客列表
        roadCondition:道路条件,拥堵程度 每小时拥堵程度
        maxSpeed:最大速度
        particlesNum:粒子数
        '''
        self.particles = [Particle(vehicleNum, len(customers))
                          for _ in range(particlesNum)]
        self.global_best = []

        self.parameter = {'vehicleNum': vehicleNum,
                          'capacity': capacity, 'customers': customers}

    def optimize(self, optimizeFunction, dominateFunction, iterations):
        '''
        optimizeFunction:优化函数
        dominateFunction:支配函数
        iterations:迭代次数
        '''
        for _ in range(iterations):
            for particle in self.particles:
                vehicleRes, departureTime = particle.decode(particle.position)
                cost, satisfy = optimizeFunction(
                    vehicleRes, departureTime, self.parameter['customers'], self.parameter['roadCondition'], self.parameter['maxSpeed'])
                particle.updateBest(
                    particle.position, cost, satisfy, dominateFunction)
            
            nonDominate=[x.packagePosAndScore() for x in self.particles]
            nonDominate=FastNondominatedSort.fast_non_dominated_sort(nonDominate,dominateFunction)
            self.global_best=self.global_best+nonDominate
            self.global_best=FastNondominatedSort.fast_non_dominated_sort(self.global_best,dominateFunction)
                

            for particle in self.particles:
                particle.update_velocity(self.global_best)
                particle.update_position()
