import queue

# 初始化队列
from threading import Thread

q = queue.Queue()

# 生产者线程向队列中插入消息
def producer():
    while True:
        item = produce_item()  # 生产一条消息
        q.put(item)
        print('生产了', item)

# 消费者线程从队列中获取消息并处理
def consumer():
    while True:
        item = q.get()     # 获取一条消息
        process_item(item) # 处理消息
        print('处理了', item)

# 启动生产者和消费者线程
p = Thread(target=producer)
c = Thread(target=consumer)
p.start()
c.start()