import queue
import threading
import time
import os
from tqdm import tqdm


file_list = os.listdir('../result')
file_path_list = [os.path.join(os.getcwd(), '../result', file) for file in file_list]
# print(file_path_list)

# 清空已有
for file in os.listdir():
    if not file.endswith('.py'):
        file_path = os.path.join(os.getcwd(), file)
        os.remove(file_path)


threadList = ['Thread-{}'.format(i) for i in range(48)]  # 8
nameList = file_path_list
queueLock = threading.Lock()
workQueue = queue.Queue()
pbar = tqdm(total=len(nameList))
exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.exitFlag = 0

    def run(self):
        # print("Starting " + self.name)
        process_data(self.name, self.q)
        # print("Exiting " + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            pbar.update(1)
            # print("%s processing %s" % (threadName, data))
            os.system('xelatex {}'.format(data))
        else:
            queueLock.release()
        time.sleep(1)


threads = []
threadID = 1
# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 创建新线程
start = time.time()
for tName in threadList:
    # print(tName)
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
end = time.time()
print('执行时间：{}'.format(end - start))
print("Exiting Main Thread")

# 34
# 执行时间：10053.052034854889
# Exiting Main Thread
# 100%|████████████████████████████████████████████████████████████████████████| 100000/100000 [2:47:33<00:00,  9.95it/s]

# 48
# 执行时间：10201.221162557602
# Exiting Main Thread
# 100%|██████████████████████████████████████████████████████████████| 100000/100000 [2:50:01<00:00,  9.80it/s


