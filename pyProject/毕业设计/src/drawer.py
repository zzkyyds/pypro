import matplotlib.pyplot as plt


def drawXY(x_coords, y_coords):
    # 使用 Matplotlib 绘制图形
    plt.scatter(x_coords[0], y_coords[0], color='red', label='First Point')  # 第一个点用红色
    plt.scatter(x_coords[1:], y_coords[1:], color='blue', label='Other Points')  # 其他点用蓝色
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Scatter Plot of Points')
    plt.grid(True)
    plt.legend()  # 添加图例
    plt.show()