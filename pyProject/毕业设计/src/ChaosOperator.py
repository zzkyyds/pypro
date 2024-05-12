import random
from matplotlib import pyplot as plt
import numpy as np
import drawer




def chaos(count:int):
    zeros=np.zeros(count)


def logisticsChaos(miu:float,seed:float,count:int)->np.ndarray:
    '''
    x(n+1)=miu*x(n)*(1-x(n))
    根据miu与zi的分布图显示,miu在(3.57,4)处于混沌状态
    img=logistics.png
    '''
    zeros=np.zeros(count)
    zeros[0]=seed
    for i in range(1,count):
        zeros[i]=miu*zeros[i-1]*(1-zeros[i-1])
    return zeros



def logisticsSineChaos(miu:float,seed:float,count:int)->np.ndarray:
    '''
    x(n+1)=miu*x(n)*(1-x(n))+(4-miu)*sin(pi*x(n))/4
    '''
    zeros=np.zeros(count)
    zeros[0]=seed
    for i in range(1,count):
        zeros[i]=miu*zeros[i-1]*(1-zeros[i-1])+(4-miu)*np.sin(np.pi*zeros[i-1])/4
    return zeros


def CubicChaos(miu:float,seed:float,count:int)->np.ndarray:
    '''
    x(n+1)=miu*x(n)(1-x(n)^2)
    '''
    zeros=np.zeros(count)
    zeros[0]=seed
    for i in range(1,count):
        zeros[i]=miu*zeros[i-1]*(1-zeros[i-1]**2)
    return zeros

def LogisticMap():
    mu = np.arange(0.0001, 4, 0.0001)
    x = 0.2  # 初值
    iters = 1000  # 不进行输出的迭代次数
    last = 100  # 最后画出结果的迭代次数
    for i in range(iters+last):
        x = mu * x * (1 - x)
        if i >= iters:
            plt.plot(mu, x, ',k', alpha=0.25)  # alpha设置透明度
    plt.show()


def show(nd:np.ndarray):
    length=len(nd)
    li=nd.tolist()
    print(li)
    xs=[x for x in range(length)]
    drawer.drawXY(xs,li)







if __name__=='__main__':
    # LogisticMap()
    logistics=logisticsSineChaos(3.831,0.6,100)
    show(logistics)