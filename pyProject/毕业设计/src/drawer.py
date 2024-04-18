import matplotlib.pyplot as plt


def drawXY(x_coords, y_coords):
    '''
    test
    '''
    # 使用 Matplotlib 绘制图形
    plt.scatter(x_coords[0], y_coords[0], color='red',
                label='First Point')  # 第一个点用红色
    plt.scatter(x_coords[1:], y_coords[1:], color='blue',
                label='Other Points')  # 其他点用蓝色
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Scatter Plot of Points')
    plt.grid(True)
    plt.legend()  # 添加图例
    plt.show()


def drawPath(xs: list, ys: list, paths: dict[dict], maxShow: int):
    '''
    画出路径
    paths是decoding的结果
    '''
    colors = ['#66ccff', 'green', 'yellow', 'black',
              'pink', 'orange', 'purple', 'brown', 'gray']
    plt.scatter(xs[0], ys[0], color='red', label='First Point')  # 第一个点用红色
    plt.scatter(xs[1:], ys[1:], color='blue', label='Other Points')  # 其他点用蓝色
    for num, path in paths.items():
        if maxShow < 0:
            continue
        maxShow -= 1
        p = [0]+path['route']+[0]
        xp = [xs[j] for j in p]
        yp = [ys[j] for j in p]
        plt.plot(xp, yp, color=colors[(num-1) % len(colors)])

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Scatter Plot of Points')
    plt.grid(True)
    plt.legend()  # 添加图例
    plt.show()


def drawTest(customers: list, vehicleRes: dict[dict], maxShow: int = 3):
    '''
    参数转换层
    '''
    xs = [i['x'] for i in customers]
    ys = [i['y'] for i in customers]
    drawPath(xs, ys, vehicleRes, maxShow)


if __name__ == '__main__':
    xs = [1, 20, 24, 32, 40, 64, 112, 160]
    ys = [109455, 5453, 4591, 3502, 2732, 1750, 986, 774]
    ks = [x*y for x, y in zip(xs, ys)]
    drawXY(xs, ks)
