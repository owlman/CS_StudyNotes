#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    操作系统多线程示例
    
    Created on 2014-1-28
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   example_threading
'''

import time
import threading
import os
import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from pathlib import Path

class ThreadSafeCounter:
    """线程安全的计数器"""
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        """线程安全的递增"""
        with self._lock:
            self.value += 1
            return self.value
    
    def get_value(self):
        """获取当前值"""
        with self._lock:
            return self.value

def basic_threading_example():
    """基本线程示例"""
    print("=== 基本线程示例 ===")
    
    def loop():
        """线程执行的函数"""
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

def worker_threads_example():
    """工作线程示例"""
    print("\n=== 工作线程示例 ===")
    
    def worker(worker_id, counter, results_queue):
        """工作线程函数"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始工作...')
        
        for i in range(3):
            current_count = counter.increment()
            result = f'Worker-{worker_id} 操作 {i+1}: 计数器 = {current_count}'
            print(f'{thread_name}: {result}')
            results_queue.put(result)
            
            # 模拟工作负载
            time.sleep(random.uniform(0.1, 0.5))
        
        final_result = f'{thread_name} 工作完成，最终计数: {counter.get_value()}'
        results_queue.put(final_result)
        print(final_result)
    
    # 创建共享资源
    counter = ThreadSafeCounter()
    results_queue = Queue()
    threads = []
    
    # 创建多个工作线程
    for i in range(3):
        thread = threading.Thread(
            target=worker, 
            args=(i, counter, results_queue),
            name=f'Worker-{i}'
        )
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 显示结果
    print(f"\n所有工作完成，最终计数器值: {counter.get_value()}")
    print("收集到的结果:")
    while not results_queue.empty():
        print(f"  {results_queue.get()}")

def file_processing_threads():
    """文件处理线程示例"""
    print("\n=== 文件处理线程示例 ===")
    
    def process_file(file_path, result_queue):
        """处理单个文件"""
        thread_name = threading.current_thread().name
        
        try:
            # 模拟文件处理
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            processing_time = random.uniform(0.5, 2.0)
            
            print(f'{thread_name} 开始处理文件: {file_path.name}')
            time.sleep(processing_time)  # 模拟处理时间
            
            result = {
                'file': str(file_path.name),
                'size': file_size,
                'processing_time': processing_time,
                'thread': thread_name
            }
            result_queue.put(result)
            print(f'{thread_name} 完成处理文件: {file_path.name}')
            
        except Exception as e:
            error_result = {
                'file': str(file_path.name),
                'error': str(e),
                'thread': thread_name
            }
            result_queue.put(error_result)
    
    # 获取当前目录下的文件
    current_dir = Path.cwd()
    files = [f for f in current_dir.iterdir() if f.is_file()][:5]  # 限制文件数量
    
    if not files:
        print("当前目录没有文件可处理")
        return
    
    result_queue = Queue()
    threads = []
    
    # 创建线程池处理文件
    max_threads = min(len(files), 3)  # 最多3个线程
    
    for i, file_path in enumerate(files):
        thread = threading.Thread(
            target=process_file,
            args=(file_path, result_queue),
            name=f'FileProcessor-{i}'
        )
        threads.append(thread)
        thread.start()
        
        # 限制并发线程数
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads.clear()
    
    # 等待剩余线程
    for thread in threads:
        thread.join()
    
    # 显示处理结果
    print(f"\n文件处理结果:")
    total_size = 0
    total_time = 0
    
    while not result_queue.empty():
        result = result_queue.get()
        if 'error' in result:
            print(f"  错误处理 {result['file']}: {result['error']}")
        else:
            print(f"  {result['file']}: {result['size']} bytes, "
                  f"耗时 {result['processing_time']:.2f}s (线程: {result['thread']})")
            total_size += result['size']
            total_time += result['processing_time']
    
    print(f"\n总计: {len(files)} 个文件, {total_size} bytes, 总耗时 {total_time:.2f}s")

def thread_pool_example():
    """线程池示例"""
    print("\n=== 线程池示例 ===")
    
    def cpu_bound_task(n):
        """CPU密集型任务"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始计算斐波那契数列第 {n} 项')
        
        def fibonacci(x):
            if x <= 1:
                return x
            return fibonacci(x-1) + fibonacci(x-2)
        
        start_time = time.time()
        result = fibonacci(n)
        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f'{thread_name} 完成计算，结果: {result}, 耗时: {processing_time:.2f}s')
        
        return {'n': n, 'result': result, 'time': processing_time, 'thread': thread_name}
    
    # 使用线程池执行任务
    numbers = [30, 32, 28, 31, 29]  # 斐波那契数列项数
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        print(f"使用线程池处理 {len(numbers)} 个任务...")
        
        # 提交所有任务
        futures = [executor.submit(cpu_bound_task, n) for n in numbers]
        
        # 收集结果
        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f'任务执行出错: {e}')
    
    # 显示汇总结果
    print(f"\n线程池执行结果:")
    total_time = sum(r['time'] for r in results)
    for result in results:
        print(f"  斐波那契({result['n']}) = {result['result']}, "
              f"耗时 {result['time']:.2f}s (线程: {result['thread']})")
    print(f"总耗时: {total_time:.2f}s")

def producer_consumer_example():
    """生产者-消费者示例"""
    print("\n=== 生产者-消费者示例 ===")
    
    def producer(queue, item_count):
        """生产者线程"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始生产 {item_count} 个项目...')
        
        for i in range(item_count):
            item = f'项目-{i+1}'
            queue.put(item)
            print(f'{thread_name} 生产: {item}')
            time.sleep(random.uniform(0.1, 0.3))
        
        # 发送结束信号
        for _ in range(2):  # 两个消费者
            queue.put(None)
        print(f'{thread_name} 生产完成')
    
    def consumer(queue, consumer_id):
        """消费者线程"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} (消费者-{consumer_id}) 开始消费...')
        
        consumed_count = 0
        while True:
            item = queue.get()
            if item is None:  # 结束信号
                break
            
            print(f'{thread_name} (消费者-{consumer_id}) 消费: {item}')
            time.sleep(random.uniform(0.2, 0.5))
            consumed_count += 1
        
        print(f'{thread_name} (消费者-{consumer_id}) 消费完成，共消费 {consumed_count} 个项目')
    
    # 创建队列和线程
    item_queue = Queue()
    item_count = 8
    
    producer_thread = threading.Thread(
        target=producer,
        args=(item_queue, item_count),
        name='Producer'
    )
    
    consumer_threads = []
    for i in range(2):
        consumer_thread = threading.Thread(
            target=consumer,
            args=(item_queue, i+1),
            name=f'Consumer-{i+1}'
        )
        consumer_threads.append(consumer_thread)
    
    # 启动所有线程
    producer_thread.start()
    for consumer_thread in consumer_threads:
        consumer_thread.start()
    
    # 等待所有线程完成
    producer_thread.join()
    for consumer_thread in consumer_threads:
        consumer_thread.join()

def thread_synchronization_example():
    """线程同步示例"""
    print("\n=== 线程同步示例 ===")
    
    class BankAccount:
        """银行账户类"""
        def __init__(self, balance):
            self.balance = balance
            self._lock = threading.Lock()
        
        def deposit(self, amount):
            """存款"""
            with self._lock:
                old_balance = self.balance
                time.sleep(0.01)  # 模拟处理时间
                self.balance = old_balance + amount
                print(f'存款 {amount}, 余额: {self.balance}')
        
        def withdraw(self, amount):
            """取款"""
            with self._lock:
                if self.balance >= amount:
                    old_balance = self.balance
                    time.sleep(0.01)  # 模拟处理时间
                    self.balance = old_balance - amount
                    print(f'取款 {amount}, 余额: {self.balance}')
                    return True
                else:
                    print(f'取款 {amount} 失败，余额不足')
                    return False
        
        def get_balance(self):
            """获取余额"""
            with self._lock:
                return self.balance
    
    def banking_operations(account, operation_count):
        """银行操作"""
        thread_name = threading.current_thread().name
        print(f'{thread_name} 开始执行 {operation_count} 次操作...')
        
        for i in range(operation_count):
            if random.random() < 0.6:  # 60%概率存款
                amount = random.randint(10, 100)
                account.deposit(amount)
            else:  # 40%概率取款
                amount = random.randint(10, 50)
                account.withdraw(amount)
        
        print(f'{thread_name} 操作完成')
    
    # 创建银行账户
    account = BankAccount(1000)
    print(f"初始余额: {account.get_balance()}")
    
    # 创建多个线程进行银行操作
    threads = []
    operation_count = 5
    
    for i in range(3):
        thread = threading.Thread(
            target=banking_operations,
            args=(account, operation_count),
            name=f'Customer-{i+1}'
        )
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print(f"\n最终余额: {account.get_balance()}")

def main():
    """主函数"""
    print("操作系统多线程示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        basic_threading_example()
        worker_threads_example()
        file_processing_threads()
        thread_pool_example()
        producer_consumer_example()
        thread_synchronization_example()
        
        print("\n" + "=" * 50)
        print("所有多线程示例执行完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()