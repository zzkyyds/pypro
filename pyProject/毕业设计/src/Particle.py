import math
import LevyFly
import numpy as np
import util


class Particle:
    '''
    编码方式参考
    https://mp.weixin.qq.com/s?__biz=MzU2NDc1MTE3Mg==&mid=2247491991&idx=1&sn=a92623b24a8a41b03774e6a3f410dadd&chksm=fc449fbccb3316aa5829c0079cccc433122bea8377afd5f3760c7b7a7390a8f5e849198dddca&scene=21#wechat_redirect

    Xv表示各个顾客对应的车辆编号,Xr表示各个顾客在对应的车辆路径中的执行次序。
    假设顾客数目为L,车辆最大使用数目为M,则Xv中每个位置上的元素都应该为1~M的随机数,Xr中每个位置上的元素都应该为1~L的随机数。

    e.g.
    Xv = [1, 2, 3, 1, 2, 3] 
    Xr = [1, 2, 3, 4, 5, 6]
    1:0->1->4->0
    2:0->2->5->0
    3:0->3->6->0

    postion = [Xv, Xr, Xt], Xv表示各个顾客对应的车辆编号,Xr表示各个顾客在对应的车辆路径中的执行次序,Xt表示每个车辆的出发时间。
    postion=[(1,客户数量,这个有数字限制),(1,客户数量),(1,车辆数量)]
    velocity 同理
    '''

    def __init__(self):
        self.parameter = {}
        self.position = []
        self.velocity = []
        self.best_position = []
        self.satisfy = 0
        self.cost = 0

    # todo 初始化考虑logistics混沌映射增加随机性
    @staticmethod
    def create(vehicleNum: int, customerNum: int):
        p = Particle()
        p.parameter = {'vehicleNum': vehicleNum, 'customerNum': customerNum}

        p.position.append(np.random.randint(1, vehicleNum+1, customerNum))
        p.position.append(np.random.rand(customerNum)*10)
        p.position.append(np.random.rand(vehicleNum)*10)

        p.velocity.append(np.random.randint(1, vehicleNum//2+1, customerNum))
        p.velocity.append(np.random.rand(customerNum))
        p.velocity.append(np.random.rand(vehicleNum))

        return p

    def toInfo(self):
        v = Particle.decode(self.position)

        res = {"vehicle": v,
               "cost": self.cost, "satisfy": self.satisfy}
        return res

    def __str__(self):
        res = self.toInfo()
        bestPos = [x.toInfo() for x in self.best_position]
        res['best'] = bestPos
        return repr(res)

    # todo 优化对于多个最佳的学习 目前是随机选择，可选算法有轮盘赌
    def update_velocity(self, global_best: list, w=0.7, c1=1.4, c2=1.4, beta=0.5):
        rc1 = np.random.randint(0, len(self.best_position))
        rc2 = np.random.randint(0, len(global_best))
        for i in range(0, 3):

            # # 莱维飞行
            # r1 = LevyFly.levy(beta)
            # r1 = util.logAbsWithSign(r1)
            # r2 = LevyFly.levy(beta)
            # r2 = util.logAbsWithSign(r2)

            # 简单随机
            r1 = np.random.random()
            r2 = np.random.random()
            cognitive_velocity = c1 * r1 * \
                (self.best_position[rc1].position[i] - self.position[i])
            social_velocity = c2 * r2 * \
                (global_best[rc2].position[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + \
                cognitive_velocity + social_velocity

    def update_position(self):
        self.position = [self.position[i] + self.velocity[i]
                         for i in range(0, 3)]
        self.position[0] = np.mod(
            self.position[0], self.parameter['vehicleNum']+1).astype(int)
        self.position[0] = np.clip(
            self.position[0], 1, self.parameter['vehicleNum']).astype(int)
        self.position[2] = np.array(
            [x if x > 0 else 0 for x in self.position[2]])

    def encode(self, vechleRes: dict) -> list:
        '''
        编码器
        '''
        pass

    @staticmethod
    def decode(position: list) -> dict[dict]:
        '''
        解码器
        返回车辆路径和车辆出发时间
        todo 时间解码没做

        return:dict[route,time]
        '''
        vehicleRes = {}

        # 客户从1开始计数，所以+1
        map = {}
        for i, v in enumerate(position[0]):
            if v not in map:
                map[v] = []
            map[v].append([i+1, position[1][i]])
        for k, v in map.items():
            v.sort(key=lambda x: x[1])
            vehicleRes[k] = {"route": [x[0]
                                       for x in v], "time": position[2][k-1]}

        return vehicleRes

    def updateBest(self, cost: float, satisfy: float, dominateFunction):
        '''
        更新当前cost和satisfy
        更新best
        '''
        self.cost = cost
        self.satisfy = satisfy

        p = util.copyWithProp(self, include=['position', 'cost', 'satisfy'])

        dominate = [
            x for x in self.best_position if dominateFunction(p, x) == 1]
        beDominate = [
            x for x in self.best_position if dominateFunction(p, x) == -1]

        if len(beDominate) == 0:
            self.best_position = [
                x for x in self.best_position if x not in dominate]
            self.best_position.append(p)

    @staticmethod
    def koptRoute(path: list, kMax=3) -> list[tuple]:
        '''
        k-opt
        有2^(k-1)*(k-1)!种可能

        确保输入的route有足够的边用于切割
        end.end和start.start链接,是同一个链,mid为其他链子

        最底层元素为客户点
        然后为总的路径
        然后为所有可能路径
        '''
        res = []

        dilimeter = util.getRandomRangedInt(len(path)+1, kMax)
        dilimeter.sort(reverse=True)
        path = [0]+path+[0]
        dilimeterRes = []
        for x in dilimeter:
            dilimeterRes.append(path[x+1:])
            path = path[:x+1]
        start = path
        end = dilimeterRes[0]
        mid = dilimeterRes[1:]
        all = util.allPermutationsReverseOrNot(mid)
        for e in all:
            nPath = []
            nPath += start
            for x in e:
                nPath += x
            nPath += end
            nPath=tuple(nPath[1:-1])
            res.append(nPath)
        res=list(set(res))
        return res

    def koptCombine(self, kMax=3) -> list[dict]:
        '''
        使用kopt优化路径
        '''
        res = {}
        vehicleRes = Particle.decode(self.position)
        for k, v in vehicleRes.items():
            route = v['route']
            time = v['time']
            allRoute = Particle.koptRoute(route, kMax=kMax)
            allVehicleRes = [{"route": a, "time": time} for a in allRoute]
            res[k] = allVehicleRes
        return res
