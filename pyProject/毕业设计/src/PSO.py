import copy
import numpy as np


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

    # todo 初始化考虑logistics混沌映射增加随机性
    def __init__(self, vehicleNum: int, customerNum: int):
        self.parameter = {'vehicleNum': vehicleNum, 'customerNum': customerNum}

        self.position = []
        self.position.append(np.random.randint(1, vehicleNum+1, customerNum))
        self.position.append(np.random.rand(customerNum)*10)
        self.position.append(np.random.rand(vehicleNum)*10)

        self.velocity = []
        self.velocity.append(np.random.randint(
            1, vehicleNum//2+1, customerNum))
        self.velocity.append(np.random.rand(customerNum))
        self.velocity.append(np.random.rand(vehicleNum))

        self.best_position = [copy.deepcopy(self.position)]

    # todo 优化对于多个最佳的学习 目前是随机选择，可选算法有轮盘赌
    def update_velocity(self, global_best: list, w=0.7, c1=1.4, c2=1.4):
        rc1 = np.random.randint(0, len(self.best_position))
        rc2 = np.random.randint(0, len(global_best))
        for i in range(0, 3):
            r1 = np.random.rand()
            r2 = np.random.rand()
            cognitive_velocity = c1 * r1 * \
                (self.best_position[rc1][i] - self.position[i])
            social_velocity = c2 * r2 * \
                (global_best[rc2][i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + \
                cognitive_velocity + social_velocity

    # todo 更新后把个人历史最佳的被支配解删除
    def update_position(self):
        self.position = [self.position[i] + self.velocity[i]
                         for i in range(0, 3)]
        self.position[0] = np.mod(
            self.position[0], self.parameter['vehicleNum']).astype(int)

    def encode(self):
        return None

    def decode(self,position:list)->dict:
        '''
        解码器
        '''
        vechileRes={}

        map= {}
        for i,v in enumerate(position[0]):
            if v not in map:
                map[v] = []
            map[v].append([i,position[1][i]])
        for k,v in map.items():
            v.sort(key=lambda x:x[1])
            vechileRes[k] = [x[0] for x in v]

        return vechileRes


class PSO:
    def __init__(self, dim, minx, maxx, n_particles):
        self.particles = [Particle(dim, minx, maxx)
                          for _ in range(n_particles)]
        self.global_best = np.random.uniform(low=minx, high=maxx, size=dim)
        self.global_best_score = -np.inf

    def optimize(self, function, iterations):
        for _ in range(iterations):
            for particle in self.particles:
                score = function(particle.position)
                if score > particle.best_score:
                    particle.best_score = score
                    particle.best_position = np.copy(particle.position)
                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best = np.copy(particle.position)
            for particle in self.particles:
                particle.update_velocity(self.global_best)
                particle.update_position(self.minx, self.maxx)
