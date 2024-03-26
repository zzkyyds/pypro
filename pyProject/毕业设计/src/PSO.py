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
        draw,adaptiveCoordinates=是否开启绘画,是否采用自适应坐标轴
        '''
        if draw:
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams["axes.unicode_minus"] = False
            fig, axs = plt.subplots()
            scat1 = axs.scatter([], [], c='b', marker='o', alpha=0.3, s=3, label="pbest")
            scat2 = axs.scatter([], [], c='r', marker='o', alpha=0.9, s=20, label="pareto")
            scat3 = axs.scatter([], [], c='g', marker='o', alpha=0.3, s=3, label="now")
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
            costMin=min([x.cost for x in self.global_best])
            sMin=min([x.satisfy for x in self.global_best])
            print(f"第{_+1}次进化,{len(self.global_best)}个最优,最小cost={costMin},最小satisfy={sMin}")
            if draw:
                pBest=[]
                for p in self.particles:
                    pBest+=p.best_position
                scat1.set_offsets([[x.cost,x.satisfy] for x in pBest])
                scat2.set_offsets([[x.cost,x.satisfy] for x in self.global_best])
                scat3.set_offsets([[x.cost,x.satisfy] for x in self.particles])
                axs.set_title(f"第{_+1}次进化")

                if adaptiveCoordinates:
                    minx=0
                    maxx=0.5
                    all_positions = [[x.cost, x.satisfy] for x in self.global_best]
                    num=len(all_positions)
                    minx=int(minx*num)
                    maxx=int(maxx*num)+1

                    xl=sorted(all_positions,key=lambda x:x[0])
                    xl=xl[minx:maxx]
                    min_x = min(pos[0] for pos in xl)
                    max_x = max(pos[0] for pos in xl)

                    yl=sorted(all_positions,key=lambda x:x[1])
                    min_y = min(pos[1] for pos in yl)
                    max_y = max(pos[1] for pos in yl)

                    axs.set_xlim(min_x * 0.8, max_x * 1.5)
                    axs.set_ylim(min_y * 0.8, max_y * 1.5)

                plt.legend()
                plt.pause(0.1)
            
