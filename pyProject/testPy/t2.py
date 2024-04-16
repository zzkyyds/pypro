import copy
from itertools import permutations, product
import random


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
    n = len(arr)
    per = list(permutations(arr))
    binary = list(product([False, True], repeat=n))
    for p in per:
        for bList in binary:
            res.append([x if b else x[::-1] for x,b in zip(p,bList)])
    return res

def koptRoute(path: list, kMax=3)->list[list]:
    '''
    k-opt
    有2^(k-1)*(k-1)!种可能

    确保输入的route有足够的边用于切割
    end.end和start.start链接,是同一个链,mid为其他链子

    最底层元素为客户点
    然后为总的路径
    然后为所有可能路径
    '''
    res=[]

    dilimeter = getRandomRangedInt(len(path)+1, kMax)
    dilimeter.sort(reverse=True)
    path = [0]+path+[0]
    dilimeterRes=[]
    for x in dilimeter:
        dilimeterRes.append(path[x+1:])
        path = path[:x+1]
    print("dilimeterRes",dilimeterRes+path)
    start=path
    end=dilimeterRes[0]
    mid=dilimeterRes[1:]
    mid=[tuple(x) for x in mid]
    all=allPermutationsReverseOrNot(mid)
    print("all",all)
    for e in all:
        nPath=[]
        nPath+=start
        for x in e:
            nPath+=x
        nPath+=end
        nPath=tuple(nPath[1:-1])
        res.append(nPath)
    res=list(set(res))
    return res


p=[1,3,4,5,2,6]
res=koptRoute(p,kMax=4)
for x in res:
    print(x)
