import matplotlib.pyplot as plt

# 给定的一组 (x, y) 坐标点
x_coords = [1, 2, 3, 4, 5]
y_coords = [2, 3, 4, 5, 6]

# 创建一个图形对象和坐标系对象
fig, ax = plt.subplots()

# 在坐标系对象中绘制 (x, y) 坐标点
ax.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')  # 设置点的样式为圆点，线的样式为实线，颜色为蓝色

# 添加标题和坐标轴标签
ax.set_title('Plot of Points')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')

# 显示网格
ax.grid(True)

# 显示图形
plt.show()
