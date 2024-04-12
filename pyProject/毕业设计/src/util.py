from itertools import permutations, product
import math
import random


def copyWithProp(obj: object, include: list = [], exclude: list = []) -> object:
    # 创建一个新的空对象
    new_obj = obj.__class__()

    # 遍历对象的所有属性
    for attr_name in dir(obj):
        # 排除私有属性和特殊方法
        if not attr_name.startswith('__'):
            # 如果 include 非空，仅复制指定属性
            if attr_name not in include:
                continue
            # 如果 exclude 非空，排除指定属性
            if attr_name in exclude:
                continue
            # 复制属性值
            setattr(new_obj, attr_name, getattr(obj, attr_name))

    return new_obj


def dominates(a, b) -> int:
    '''
    比较两个个体的支配关系
    '''
    if a.cost == b.cost and a.satisfy == b.satisfy:
        return 0
    if a.cost <= b.cost and a.satisfy <= b.satisfy:
        return 1
    if a.cost >= b.cost and a.satisfy >= b.satisfy:
        return -1

    return 0


def logAbsWithSign(x):
    return math.copysign(1, x)*math.log(abs(x)+1)


def getHybercube(bestList: list) -> list:
    '''
    获取历史最优的超立方体分割,并且包含计数和粒子序数
    '''
    pass


def getRandomRangedInt(n, count: int):
    '''
    从[0,1,2,...,n-1]中无放回选取count个数字返回
    如果元素不够,则返回所有元素
    '''
    if count >= n+1:
        return list(range(0, n))
    return random.sample(range(0, n), count)


def allPermutationsReverseOrNot(arr: list[list])->list[list[list]]:
    '''
    获取数组的所有排列,并且有反转或者不反转
    总计2^n*n!
    '''
    if len(arr) == 0:
        return []
    if len(arr) == 1:
        return arr+[arr[0][::-1]]
    # 太大了,不考虑
    if len(arr) >= 6:
        return []
    res = []
    eLen = len(arr[0])
    per = list(permutations(arr))
    binary = list(product([False, True], repeat=eLen))
    for p in per:
        for bList in binary:
            res.append([x if b else x[::-1] for x,b in zip(p,bList)])
    return res
