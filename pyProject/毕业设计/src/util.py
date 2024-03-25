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


def getHybercube(bestList:list)->list:
    '''
    获取历史最优的超立方体分割,并且包含计数和粒子序数
    '''
    pass



