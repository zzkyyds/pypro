from itertools import islice, product
import random
from matplotlib import pyplot as plt
from Particle import Particle
import FastNondominatedSort
import util
import ThreadPoolUtil


class PSO:
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
        self.kopt = []

        self.parameter = {'vehicleNum': vehicleNum, 'capacity': capacity,
                          'customers': customers, 'roadCondition': roadCondition, 'maxSpeed': maxSpeed}
        self.tp = ThreadPoolUtil.getThreadPool()

    def koptScore(self, particle: Particle, vehicleRess: dict[list[dict]], optimizeFunction, dominateFunction,countMax=200):
        '''
        计算kopt的分数并返回非支配解

        para:
        vehicleRess=车辆编号->所有可能的路径(每一个路径由字典表示,包含route,time,vehicleNum)
        '''
        def create_particle(iterator):
            i,c=iterator
            newP = Particle.createEmpty()
            newP.cost = i.cost + c.cost
            newP.satisfy = i.satisfy + c.satisfy
            newP.tmp = {**i.tmp, **c.tmp}
            return newP
        def createParticleByList(l:list):
            newP=Particle.createEmpty()
            newP.cost = sum([i.cost for i in l])
            newP.satisfy = sum([i.satisfy for i in l])
            tmpD={}
            for i in l:
                tmpD.update(i.tmp)
            newP.tmp=tmpD
            return newP

        def update_position(c1):
            c1.position = c1.encode(particle.parameter, c1.tmp)
            return c1

        tp = self.tp
        d = {}
        ps = []
        for k1, v1 in vehicleRess.items():
            d[k1] = []
            ps += v1
        results = tp.map(lambda p: optimizeFunction(
            {p['vehicleNum']: p}, self.parameter['customers'], self.parameter['roadCondition'], self.parameter['maxSpeed']), ps)
        for i, (cost, satisfy) in enumerate(results):
            e = Particle.createEmpty()
            e.cost = cost
            e.satisfy = satisfy
            e.tmp = {}
            vNum = ps[i]['vehicleNum']
            e.tmp[vNum] = ps[i]
            d[vNum].append(e)
        results = tp.map(lambda item: {item[0]: FastNondominatedSort.non_dominated_sort(
            item[1], dominateFunction)}, d.items())
        d = {}
        for r in results:
            d.update(r)

        combination=[]
        for k2, v2 in d.items():
            if len(combination) == 0:
                combination += v2
                continue
            iteration = [(i, c) for i in v2 for c in combination]
            results=list(tp.map(create_particle, iteration))
            combination = FastNondominatedSort.non_dominated_sort(
                results, dominateFunction)
            combination = combination[0:countMax]


        # vs=d.values()
        # combination = [list(comb) for comb in islice(product(*vs), countMax)]
        # results=tp.map(lambda c:createParticleByList(c),combination)
        # combination = FastNondominatedSort.non_dominated_sort(list(results), dominateFunction)

        for c1 in combination:
            c1.position = c1.encode(particle.parameter, c1.tmp)

        results = tp.map(update_position, combination)
        for r in results:
            pass

        return combination

    def optimize(self, optimizeFunction, dominateFunction, iterations, draw=False, adaptiveCoordinates=False,kopt=5,kCount=30):
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
            scat1 = axs.scatter([], [], c='b', marker='o',
                                alpha=0.3, s=3, label="pbest")
            scat2 = axs.scatter([], [], c='r', marker='o',
                                alpha=0.9, s=20, label="pareto")
            scat3 = axs.scatter([], [], c='g', marker='o',
                                alpha=0.3, s=3, label="now")
            scat4 = axs.scatter([], [], c='#66ccff', marker='o',
                                alpha=0.9, s=20, label="kopt")
            axs.set_xlim(4e4, 1.5e5)
            axs.set_ylim(4e4, 1.5e5)

            tp = self.tp

        for _ in range(iterations):
            results = tp.map(lambda p: optimizeFunction(p.decode(p.position),
                                                        self.parameter['customers'],
                                                        self.parameter['roadCondition'],
                                                        self.parameter['maxSpeed']),
                             self.particles)
            for ii, (cost, satisfy) in enumerate(results):
                self.particles[ii].updateBest(cost, satisfy, dominateFunction)

            nonDominate = FastNondominatedSort.non_dominated_sort(
                self.particles, dominateFunction)
            nonDominate = [util.copyWithProp(
                x, include=['position', 'cost', 'satisfy', 'parameter']) for x in nonDominate]
            self.global_best = self.global_best+nonDominate
            self.global_best = FastNondominatedSort.non_dominated_sort(
                self.global_best, dominateFunction)
            for gb in self.global_best:
                if gb.koptCount>kCount:
                    continue
                gb.koptCount+=1
                vress = gb.koptCombine(kMax=kopt)
                kopts = self.koptScore(
                    gb, vress, optimizeFunction, dominateFunction)
                self.kopt += kopts
            self.kopt = FastNondominatedSort.non_dominated_sort(
                self.kopt, dominateFunction)

            results = tp.map(lambda p: p.update_velocity(
                self.kopt), self.particles)
            for result in results:
                pass
            results = tp.map(lambda p: p.update_position(), self.particles)
            for result in results:
                pass

            # 输出代际信息
            costMin = min([x.cost for x in self.kopt])
            sMin = min([x.satisfy for x in self.kopt])
            print(
                f"第{_+1}次进化,{len(self.global_best)}个帕累托,{len(self.kopt)}个kopt,最小cost={costMin},最小satisfy={sMin}")
            if draw:
                pBest = []
                for p in self.particles:
                    pBest += p.best_position
                scat1.set_offsets([[x.cost, x.satisfy] for x in pBest])
                scat2.set_offsets([[x.cost, x.satisfy]
                                  for x in self.global_best])
                scat3.set_offsets([[x.cost, x.satisfy]
                                  for x in self.particles])
                # scat4.set_offsets([[x.cost, x.satisfy] for x in self.kopt])
                axs.set_title(f"第{_+1}次进化")

                if adaptiveCoordinates:
                    minx = 0
                    maxx = 0.5
                    all_positions = [[x.cost, x.satisfy]
                                     for x in self.kopt]
                    num = len(all_positions)
                    minx = int(minx*num)
                    maxx = int(maxx*num)+1

                    xl = sorted(all_positions, key=lambda x: x[0])
                    xl = xl[minx:maxx]
                    min_x = min(pos[0] for pos in xl)
                    max_x = max(pos[0] for pos in xl)

                    yl = sorted(all_positions, key=lambda x: x[1])
                    min_y = min(pos[1] for pos in yl)
                    max_y = max(pos[1] for pos in yl)

                    axs.set_xlim(min_x * 0.8-1e3, max_x * 1.5+1e3)
                    axs.set_ylim(min_y * 0.8-1e3, max_y * 1.5+1e3)

                plt.legend()
                plt.pause(0.1)
        if draw:
            plt.close()
