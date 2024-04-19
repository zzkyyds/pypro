class MyList:
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

# 创建一个自定义的MyList对象
my_list = MyList([1, 2, 3, 4, 5])

# 使用len()函数获取MyList对象的长度
print(len(my_list))  # 输出 5
