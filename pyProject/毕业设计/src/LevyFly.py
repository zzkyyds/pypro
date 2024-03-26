import math
import numpy as np
import util
from scipy.special import gamma
import matplotlib.pyplot as plt


def levy(beta: float=1) -> float:
    alpha_u = math.pow((gamma(1+beta)*math.sin(math.pi*beta/2) /
                       (gamma(((1+beta)/2)*beta*math.pow(2, (beta-1)/2)))), (1/beta))
    alpha_v = 1
    u = np.random.normal(0, alpha_u, 1)
    v = np.random.normal(0, alpha_v, 1)
    step = u / math.pow(abs(v), (1/beta))

    return step[0]


def levyMulti(beta: float=1, count: int = 100) -> list[float]:
    alpha_u = math.pow((gamma(1+beta)*math.sin(math.pi*beta/2) /
                       (gamma(((1+beta)/2)*beta*math.pow(2, (beta-1)/2)))), (1/beta))
    alpha_v = 1
    res = []
    for _ in range(count):
        u = np.random.normal(0, alpha_u, 1)
        v = np.random.normal(0, alpha_v, 1)
        step = u / math.pow(abs(v), (1/beta))
        res.append(step[0])

    return res


def test():
    x = np.arange(1, 1000, 0.1)
    y = []
    beta = 0.5
    alpha_u = math.pow((gamma(1+beta)*math.sin(math.pi*beta/2) /
                       (gamma(((1+beta)/2)*beta*math.pow(2, (beta-1)/2)))), (1/beta))
    alpha_v = 1
    for t in x:
        u = np.random.normal(0, alpha_u, 1)
        v = np.random.normal(0, alpha_v, 1)
        step = u / math.pow(abs(v), (1/beta))
        y.append(util.logAbsWithSign(step[0]))

    plt.hist(y, bins=1000, edgecolor='black')
    plt.xlabel('Step Length')
    plt.ylabel('Frequency')
    plt.title('Distribution of Levy Flight Step Lengths')
    plt.grid(True)
    plt.show()


def show():
    xs = [0]
    ys = [0]
    x = 0
    y = 0
    for i in range(999):
        xita = math.pi*2*abs(np.random.random())
        l = levy(2)
        x += l*math.cos(xita)
        y += l*math.sin(xita)
        xs.append(x)
        ys.append(y)
    # 创建一个图形对象和坐标系对象
    fig, ax = plt.subplots()

    # 在坐标系对象中绘制 (x, y) 坐标点
    ax.plot(xs, ys, marker='o', linestyle='-',
            color='b')  # 设置点的样式为圆点，线的样式为实线，颜色为蓝色

    # 添加标题和坐标轴标签
    ax.set_title('Plot of Points')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    # 显示网格
    ax.grid(True)

    # 显示图形
    plt.show()


if __name__ == '__main__':
    test()
