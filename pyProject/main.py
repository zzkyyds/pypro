import numpy as np
import matplotlib.pyplot as plt

def func(x, xmax, xmin):
    temp_ = binary2dec(x)
    temp = xmin + (xmax-xmin)/(2**D-1) * temp_
    return temp + 6*np.sin(4*temp) + 9*np.cos(6*temp)

def binary2dec(x):
    total_value = 0
    for k in range(len(x)):
        total_value += x[k] * 2**(len(x)-k-1)
    return total_value

xx = np.arange(0, 9, 0.05)
f_x = xx + 6*np.sin(4*xx) + 9*np.cos(6*xx)
plt.figure(1)
plt.plot(xx, f_x)
plt.title('f(x)=x+6sin(4x)+9cos(6x)')
plt.xlabel('x')
plt.ylabel('f(x)')

NP = 100 # number of particles
G = 200 # number of generations
D = 10 # number of dimensions
c1 = 1.5
c2 = 1.5
w_max = 0.8
w_min = 0.4
v_max = 5
v_min = -5
x_min = 0
x_max = 9
mode = 'max' # 'min' or 'max'

x = np.random.rand(NP, D) > 0.5
v = v_min + np.random.rand(NP, D) * (v_max - v_min)

individual_best = x.copy()
if mode == 'min':
    global_best_fit = np.inf
else:
    global_best_fit = -np.inf

fitness_optimal = np.zeros(G)
for gen in range(G):
    w = w_max - (w_max - w_min) * gen / G
    for k in range(NP):
        v[k] = w * v[k] + c1 * np.random.rand() * np.logical_xor(individual_best[k],x[k]) + c2 * np.random.rand() * np.logical_xor(global_best_fit,x[k])
        v[k] = np.clip(v[k], v_min, v_max)
        vs = 1 / (1 + np.exp(-v))
        for t in range(D):
            x[k, t] = 1 if vs[k, t] > np.random.rand() else 0


    for k in range(NP):
        old_fitness = func(individual_best[k], x_max, x_min)
        new_fitness = func(x[k], x_max, x_min)
        if mode == 'min':
            if new_fitness < old_fitness:
                individual_best[k] = x[k]
                old_fitness = new_fitness
        else:
            if new_fitness > old_fitness:
                individual_best[k] = x[k]
                old_fitness = new_fitness

        if mode == 'min':
            if new_fitness < global_best_fit:
                global_best_fit = new_fitness
                global_best = individual_best[k]
        else:
            if new_fitness > global_best_fit:
                global_best_fit = new_fitness
                global_best = individual_best[k]

    fitness_optimal[gen] = global_best_fit

plt.figure(2)
plt.plot(fitness_optimal)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Fitness Value: {} | {}'.format(fitness_optimal[-1], x_min + (x_max - x_min) / (2**D-1) * binary2dec(global_best)))

plt.show()
