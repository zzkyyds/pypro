from matplotlib import pyplot as plt
from Particle import Particle
import FastNondominatedSort
import util


class PSO:
    # todo
    def __init__(self, vehicleNum: int, capacity: int, customers: list[dict], roadCondition: list, maxSpeed: float,
                 particlesNum: int):
        '''
        vehicleNum:车辆数
        capacity:车辆容量
        customers:顾客列表,包括起点,所以-1
        roadCondition:道路条件,拥堵程度 每小时拥堵程度
        maxSpeed:最大速度
        particlesNum:粒子数
        '''
        self.particles = [Particle.create(vehicleNum, len(customers)-1)
                          for _ in range(particlesNum)]
        self.global_best = []

        self.parameter = {'vehicleNum': vehicleNum, 'capacity': capacity,
                          'customers': customers, 'roadCondition': roadCondition, 'maxSpeed': maxSpeed}

    def optimize(self, optimizeFunction, dominateFunction, iterations,draw=False,adaptiveCoordinates=False):
        '''
        optimizeFunction:优化函数
        dominateFunction:支配函数
        iterations:迭代次数
        '''
        if draw:
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams["axes.unicode_minus"] = False
            fig, axs = plt.subplots()
            scat1 = axs.scatter([], [], c='b', marker='o', alpha=0.3, s=3, label="pbest")
            scat2 = axs.scatter([], [], c='r', marker='o', alpha=0.9, s=20, label="pareto")
            axs.set_xlim(4e4,1.5e5)
            axs.set_ylim(4e4,1.5e5)

        for _ in range(iterations):
            for particle in self.particles:
                vehicleRes, departureTime = particle.decode(particle.position)
                cost, satisfy = optimizeFunction(
                    vehicleRes, departureTime, self.parameter['customers'], self.parameter['roadCondition'], self.parameter['maxSpeed'])
                particle.updateBest(cost, satisfy, dominateFunction)

            nonDominate = FastNondominatedSort.non_dominated_sort(
                self.particles, dominateFunction)
            nonDominate = [util.copyWithProp(
                x, include=['position', 'cost', 'satisfy']) for x in nonDominate]
            self.global_best = self.global_best+nonDominate
            self.global_best = FastNondominatedSort.non_dominated_sort(
                self.global_best, dominateFunction)

            for particle in self.particles:
                particle.update_velocity(self.global_best)
                particle.update_position()

            #输出代际信息
            # 在 f1 上作图显示
            print(f"第{_+1}次进化,{len(self.global_best)}个最优")
            if draw:
                scat1.set_offsets([[x.cost,x.satisfy] for x in self.particles])
                scat2.set_offsets([[x.cost,x.satisfy] for x in self.global_best])
                axs.set_title(f"第{_+1}次进化")

                if adaptiveCoordinates:
                    all_positions = [[x.cost, x.satisfy] for x in self.particles + self.global_best]
                    min_x = min(pos[0] for pos in all_positions)
                    max_x = max(pos[0] for pos in all_positions)
                    min_y = min(pos[1] for pos in all_positions)
                    max_y = max(pos[1] for pos in all_positions)

                    axs.set_xlim(min_x * 0.9, max_x * 1.1)
                    axs.set_ylim(min_y * 0.9, max_y * 1.1)

                plt.legend()
                plt.pause(0.1)
            
