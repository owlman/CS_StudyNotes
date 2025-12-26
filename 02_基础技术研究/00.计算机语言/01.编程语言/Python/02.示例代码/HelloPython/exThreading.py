#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Python多线程示例
    
    Created on 2014-1-28
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   example_threading
'''

import time
import threading
import concurrent.futures
from queue import Queue

class Counter:
    """线程安全的计数器"""
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        """线程安全的递增操作"""
        with self._lock:
            self.value += 1
            return self.value
    
    def get_value(self):
        """获取当前值"""
        with self._lock:
            return self.value

def basic_thread_example():
    """基本线程示例"""
    print("=== 基本线程示例 ===")
    
    def loop():
        """新线程执行的代码"""
        current_thread = threading.current_thread()
        print(f'线程 {current_thread.name} 正在运行...')
        n = 0
        while n < 5:
            n += 1
            print(f'线程 {current_thread.name} >>> {n}')
            time.sleep(1)
        print(f'线程 {current_thread.name} 已结束.')

    print(f'主线程 {threading.current_thread().name} 正在运行...')
    
    # 创建并启动线程
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()  # 等待线程结束
    
    print(f'主线程 {threading.current_thread().name} 已结束.')

def multiple_threads_example():
    """多线程示例"""
    print("\n=== 多线程示例 ===")
    
    def worker(num, counter):
        """工作线程函数"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始工作...')
        
        for i in range(3):
            current_count = counter.increment()
            print(f'{thread_name} - 操作 {i+1}: 计数器 = {current_count}')
            time.sleep(0.5)
        
        print(f'{thread_name} 工作完成.')
        return f'{thread_name} 的结果'
    
    counter = Counter()
    threads = []
    results = []
    
    # 创建多个线程
    for i in range(3):
        thread = threading.Thread(
            target=worker, 
            args=(i, counter),
            name=f'Worker-{i}'
        )
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print(f"最终计数器值: {counter.get_value()}")

def thread_with_queue_example():
    """使用队列的生产者-消费者示例"""
    print("\n=== 生产者-消费者示例 ===")
    
    def producer(queue, items):
        """生产者线程"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始生产...')
        
        for item in items:
            print(f'{thread_name} 生产: {item}')
            queue.put(item)
            time.sleep(0.2)
        
        # 发送结束信号
        queue.put(None)
        print(f'{thread_name} 生产完成.')
    
    def consumer(queue):
        """消费者线程"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始消费...')
        
        while True:
            item = queue.get()
            if item is None:  # 结束信号
                break
            
            print(f'{thread_name} 消费: {item}')
            time.sleep(0.3)
            queue.task_done()
        
        print(f'{thread_name} 消费完成.')
    
    # 创建队列
    item_queue = Queue()
    
    # 生产的数据
    items = [f'产品-{i}' for i in range(5)]
    
    # 创建线程
    producer_thread = threading.Thread(
        target=producer, 
        args=(item_queue, items),
        name='Producer'
    )
    consumer_thread = threading.Thread(
        target=consumer, 
        args=(item_queue,),
        name='Consumer'
    )
    
    # 启动线程
    producer_thread.start()
    consumer_thread.start()
    
    # 等待完成
    producer_thread.join()
    consumer_thread.join()

def thread_pool_example():
    """线程池示例"""
    print("\n=== 线程池示例 ===")
    
    def process_task(task_id):
        """处理任务函数"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 处理任务 {task_id}')
        time.sleep(1)
        result = f'任务 {task_id} 的结果'
        print(f'{thread_name} 完成任务 {task_id}')
        return result
    
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务
        futures = [executor.submit(process_task, i) for i in range(6)]
        
        # 获取结果
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f'任务执行出错: {e}')
    
    print(f"所有任务完成，结果数量: {len(results)}")

def lock_example():
    """锁示例"""
    print("\n=== 锁示例 ===")
    
    def unsafe_increment(shared_list):
        """不安全的递增操作"""
        for i in range(1000):
            shared_list.append(i)
    
    def safe_increment(shared_list, lock):
        """安全的递增操作"""
        for i in range(1000):
            with lock:
                shared_list.append(i)
    
    # 不安全操作
    unsafe_list = []
    unsafe_threads = []
    for i in range(5):
        thread = threading.Thread(target=unsafe_increment, args=(unsafe_list,))
        unsafe_threads.append(thread)
        thread.start()
    
    for thread in unsafe_threads:
        thread.join()
    
    # 安全操作
    safe_list = []
    lock = threading.Lock()
    safe_threads = []
    for i in range(5):
        thread = threading.Thread(target=safe_increment, args=(safe_list, lock))
        safe_threads.append(thread)
        thread.start()
    
    for thread in safe_threads:
        thread.join()
    
    print(f"不安全操作结果数量: {len(unsafe_list)}")
    print(f"安全操作结果数量: {len(safe_list)}")

def daemon_thread_example():
    """守护线程示例"""
    print("\n=== 守护线程示例 ===")
    
    def background_task():
        """后台任务"""
        while True:
            print("后台任务运行中...")
            time.sleep(1)
    
    # 创建守护线程
    daemon_thread = threading.Thread(
        target=background_task,
        name='DaemonThread',
        daemon=True  # 设置为守护线程
    )
    
    daemon_thread.start()
    
    print("主线程将运行3秒...")
    time.sleep(3)
    print("主线程结束，守护线程将自动终止")

def main():
    """主函数"""
    print("Python多线程示例程序")
    print("=" * 50)
    
    try:
        # 运行各种示例
        basic_thread_example()
        multiple_threads_example()
        thread_with_queue_example()
        thread_pool_example()
        lock_example()
        daemon_thread_example()
        
        print("\n" + "=" * 50)
        print("所有示例执行完成")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()