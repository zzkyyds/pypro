import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams["axes.unicode_minus"] = False

# https://zhuanlan.zhihu.com/p/682474288

class MOPSO:
    def __init__(self, objective_function, bounds, swarm_size=50, max_iter=100, inertia_weight=0.4, num_grids=20,
                 max_len=100, draw=False, label=None):
        self.objective_function = objective_function
        self.label = label
        self.bounds = bounds
        self.swarm_size = swarm_size
        self.max_iter = max_iter
        self.inertia_weight = inertia_weight
        self.dim = len(bounds)
        self.num_grids = num_grids
        self.max_len = max_len
        self.swarm = np.hstack([np.random.uniform(low, high, (swarm_size, 1)) for low, high in bounds])
        self.velocity = np.zeros((swarm_size, self.dim))
        self.p_best = self.swarm.copy()
        self.p_best_score = np.array([self.objective_function(x) for x in self.swarm])
        self.repository = self.swarm[self.pareto(self.p_best_score)]
        self.cube = self.get_hybercube(np.array([self.objective_function(x) for x in self.repository]))

        self.draw = draw
        if self.draw:
            self.fig, axs = plt.subplots(figsize=(8, 8))
            self.ax = axs
            self.ax.set_xlim(0, 1.2)
            self.ax.set_ylim(0, 3)
            self.scat1 = self.ax.scatter([], [], c='b', marker='o', alpha=0.3, s=3, label="pbest")
            self.scat2 = self.ax.scatter([], [], c='r', marker='o', alpha=0.9, s=20, label="pareto")
            self.scat3 = self.ax.scatter([], [], c='black', marker='o', alpha=0.9, s=20, label="true")
            self.scat4 = self.ax.scatter([], [], c='g', marker='o', alpha=0.9, s=50, label="rep_h")

    def pareto(self, fitness):
        # 执行帕累托筛选，找出帕累托最优解的索引
        pareto_index = np.ones(fitness.shape[0], dtype=bool)
        for i, c in enumerate(fitness):
            if pareto_index[i]:
                pareto_index[i] = np.sum(np.all(fitness[pareto_index] <= c, axis=1)) == 1
                pareto_index[pareto_index] = np.any(fitness[pareto_index] <= c, axis=1)
        return pareto_index

    def get_hybercube(self, fitness):
        # 计算超立方体的边界
        x_min = np.min(fitness, axis=0)
        x_max = np.max(fitness, axis=0)
        grid_sizes = (x_max - x_min) / self.num_grids
        # 计算网格编码
        relative_fitness = (fitness - x_min) / grid_sizes
        grid_codes = relative_fitness.astype(int)
        return grid_codes

    def update_repository(self):
        """
        优先保留次要空间的粒子,即含粒子较少的超立方体内的粒子
        """
        fitness = np.array([self.objective_function(x) for x in self.swarm])
        cur_particles = self.swarm[self.pareto(fitness)]
        all_particles = np.vstack([self.repository, cur_particles])
        all_scores = np.array([self.objective_function(x) for x in all_particles])
        pareto_index = self.pareto(all_scores)
        self.repository = np.unique(all_particles[pareto_index], axis=0)
        self.cube = self.get_hybercube(all_scores[pareto_index])
        if len(self.repository) > self.max_len:
            def accumulate_hypercube(arr, target_sum=100):
                hypercube, counts = np.unique(arr, axis=0, return_counts=True)
                selected_indices = []
                current_sum = 0
                for i in np.argsort(counts):
                    current_sum += counts[i]
                    if current_sum >= target_sum:
                        break
                    else:
                        selected_indices.append(i)
                selected_hypercube = hypercube[selected_indices]
                return selected_hypercube

            selected_hypercube = accumulate_hypercube(self.cube)
            indices = np.where((selected_hypercube[:, None] == self.cube).all(-1))[1]
            self.repository = self.repository[indices]
            self.cube = self.cube[indices]

    def roulette_wheel_selection(self):
        """
        根据轮盘赌选择一个超立方体,在该超立方体内随机抽一个粒子作为rep[h]
        """

        def softmax(x):
            exp_x = np.exp(x - np.max(x))  # 为了数值稳定性，减去最大值
            return exp_x / np.sum(exp_x)

        hybercube, counts = np.unique(self.cube, axis=0, return_counts=True)
        scores = 10 / counts
        idx = np.random.choice(np.arange(len(scores)), p=softmax(scores))
        random_index = np.random.choice(np.where((self.cube == hybercube[idx]).all(axis=1))[0])
        return self.repository[random_index]

    def run(self):
        for _ in range(self.max_iter):
            print(_)
            for i in range(self.swarm_size):
                r1 = np.random.rand(self.dim)
                r2 = np.random.rand(self.dim)
                hypercube_particle = self.roulette_wheel_selection()
                self.velocity[i] = self.inertia_weight * self.velocity[i] \
                                   + r1 * (self.p_best[i] - self.swarm[i]) \
                                   + r2 * (hypercube_particle - self.swarm[i])
                self.swarm[i] += self.velocity[i]
                self.swarm[i] = np.array(
                    [np.clip(x, bound[0], bound[1]) for x, bound in zip(self.swarm[i], self.bounds)])

            if self.draw:
                self.scat1.set_offsets(self.p_best_score)
                self.scat2.set_offsets([self.objective_function(x) for x in self.repository])
                self.scat3.set_offsets(self.label)
                self.scat4.set_offsets(self.objective_function(hypercube_particle))
                self.ax.set_title(f"第{_+1}次进化")
                plt.legend()
                plt.pause(0.002)

            self.update_repository()
            for i in range(self.swarm_size):
                self.p_best_score[i] = self.objective_function(self.p_best[i])
                if np.all(self.objective_function(self.swarm[i]) <= self.p_best_score[i]):
                    self.p_best[i] = self.swarm[i]
        if self.draw:
            plt.show()


if __name__ == "__main__":
    def ZDT1(x):
        n = len(x)
        f1 = x[0]
        g = 1 + 9 * np.sum(x[1:]) / (n - 1)
        h = 1 - np.sqrt(f1 / g)
        f2 = g * h
        return f1, f2


    ZDT1_bounds = [(0, 1) for i in range(30)]
    zdt1_label = np.array([[1., 0.00095582],
                           [0.95666027, 0.02518556],
                           [0.90431804, 0.04989127],
                           [0.8623383, 0.07228216],
                           [0.8224121, 0.09445617],
                           [0.78483084, 0.11519835],
                           [0.7483342, 0.13668395],
                           [0.71676123, 0.15524243],
                           [0.68009687, 0.17688189],
                           [0.64965242, 0.19594608],
                           [0.61931024, 0.21463571],
                           [0.58994446, 0.2331481],
                           [0.5636035, 0.25105183],
                           [0.53686102, 0.26949325],
                           [0.51096718, 0.28708163],
                           [0.48585333, 0.30496429],
                           [0.46171245, 0.32190747],
                           [0.43857531, 0.33986237],
                           [0.4154546, 0.35728116],
                           [0.3945688, 0.3745337],
                           [0.37143588, 0.39252547],
                           [0.35054869, 0.40966841],
                           [0.32974983, 0.42778528],
                           [0.30958123, 0.44542284],
                           [0.28915394, 0.46480394],
                           [0.26910451, 0.4827566],
                           [0.25014924, 0.50104115],
                           [0.23106485, 0.52095508],
                           [0.21223078, 0.54095798],
                           [0.19209267, 0.56304973],
                           [0.17450888, 0.58357845],
                           [0.15655026, 0.60602267],
                           [0.13767779, 0.63155454],
                           [0.11911788, 0.65643775],
                           [0.10046068, 0.68523005],
                           [0.08169388, 0.71629302],
                           [0.06234464, 0.75204725],
                           [0.04295291, 0.7953892],
                           [0.02232389, 0.85364365],
                           [0., 1.00142]])
    mopso = MOPSO(ZDT1, ZDT1_bounds, draw=True, swarm_size=1500, max_iter=50, num_grids=50, max_len=300,
                  label=zdt1_label)
    mopso.run()