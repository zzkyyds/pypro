'''
Author: CloudSir
Date: 2021-08-03 15:01:17
LastEditTime: 2021-08-03 15:26:05
LastEditors: CloudSir
Description: Python拟合任意函数
https://github.com/cloudsir
'''
# 引用库函数

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as op

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 需要拟合的函数
def f_1(x, A, B, C):
    return A * x**2 + B * x + C

# 需要拟合的数据组
x_group = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11]
y_group = [2.83, 9.53, 14.52, 21.57, 38.26, 53.92, 73.15, 101.56, 129.54, 169.75, 207.59,245]

# 得到返回的A，B值
A, B, C = op.curve_fit(f_1, x_group, y_group)[0]

# 数据点与原先的进行画图比较
plt.scatter(x_group, y_group, marker='o',label='真实值')
x = np.arange(0, 15, 0.01)
y = A * x**2 + B *x + C
plt.plot(x, y,color='red',label='拟合曲线')
plt.legend() # 显示label

plt.show()
