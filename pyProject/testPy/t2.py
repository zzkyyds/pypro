import copy
from itertools import permutations, product


def allPermutationsReverseOrNot(arr: list[list]):
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
    eLen = len(arr)
    per = list(permutations(arr))
    binary = list(product([False, True], repeat=eLen))
    for p in per:
        for bList in binary:
            res.append([x if b else x[::-1] for x,b in zip(p,bList)])


    return res


a=[[1,2,3],[2,3,4]]
print(allPermutationsReverseOrNot(a))