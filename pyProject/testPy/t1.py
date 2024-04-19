from itertools import product, islice

vs = [[1, 2, 3], ['a', 'b', 'c'], ['x', 'y', 'z']]
max_combinations = 10  # 设置最大的组合数量

# 生成所有可能的组合，并在达到最大数量时停止
combinations = [list(comb) for comb in islice(product(*vs), max_combinations)]

print(combinations)
