from typing import List, Callable, Any

import numpy as np


# fixme
def fast_non_dominated_sort(values: List, dominates: Callable[[Any, Any], bool]) -> List:
    '''
    快速非支配排序
    '''
    if (len(values) == 0):
        return []
    if (len(values) == 1):
        return values.copy()

    v = values.copy()
    result = []  # 返回的结果
    now = None
    nd = []  # 非支配集合

    while True:
        flag = True
        now = v[0]
        for i in range(1, len(v)):
            res = dominates(now, v[i])
            if res == 0:
                nd.append(v[i])
            if res == -1:
                nd.append(now)
                flag = False
        if flag:
            result.append(now)
        v = nd.copy()

        if len(v) == 0:
            break
        if len(v) == 1:
            result.append(v[0])
            break

    return result


def non_dominated_sort(values: List, dominates: Callable[[Any, Any], int]) -> List:
    '''
    非支配排序,返回所有的最优解
    '''
    n = [0 for i in range(0, len(values))]

    for i in range(0, len(values)-1):
        for j in range(i+1, len(values)):
            res = dominates(values[i], values[j])
            if res == 1:
                n[j] += 1
            if res == -1:
                n[i] += 1

    result = [values[i] for i in range(len(values)) if n[i] == 0]
    return result
