from concurrent.futures import ThreadPoolExecutor
import time
import util


def getThreadPool():
    return ThreadPoolExecutor(max_workers=util.getLogicCoreCount()+1)
    # return ThreadPoolExecutor(1)

# 定义一个准备作为线程任务的函数
def action(max):
    time.sleep(1)
    print(max)
if __name__ == '__main__':
    # 创建一个包含2条线程的线程池
    pool = ThreadPoolExecutor(max_workers=util.getLogicCoreCount()+1)
    results=pool.map(action,[1,2,3,4,5,6,7,8,9,10])
    for r in results:
        print(r)

