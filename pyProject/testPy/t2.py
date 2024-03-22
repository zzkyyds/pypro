import math
import numpy as np
from scipy.special import gamma
import matplotlib.pyplot as plt

x = np.arange(1,1000,0.1)
y = []
beta = 3/2
alpha_u = math.pow((gamma(1+beta)*math.sin(math.pi*beta/2)/(gamma( ((1+beta)/2)*beta*math.pow(2,(beta-1)/2)) ) ),(1/beta))
alpha_v = 1
for t in x:
    u = np.random.normal(0,alpha_u,1)
    v = np.random.normal(0,alpha_v,1)
    step = u / math.pow(abs(v),(1/beta))

    y.append(abs(step[0]))

plt.hist(y, bins=1000, edgecolor='black')
plt.xlabel('Step Length')
plt.ylabel('Frequency')
plt.title('Distribution of Levy Flight Step Lengths')
plt.grid(True)
plt.show()


