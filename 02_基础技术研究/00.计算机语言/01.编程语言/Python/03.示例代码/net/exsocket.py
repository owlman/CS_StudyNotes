#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Python Socket编程示例
    
    Created on 2009-9-4
    Updated on 2025-11-26

    @author: lingjie
    @name : example_socket_proc
'''

import socket
import threading
import time
import sys
import argparse
from datetime import datetime

class SocketServer:
    """Socket服务器类"""
    
    def __init__(self, host="localhost", port=160214, buffer_size=1024, max_connections=5):
        """
        初始化服务器
        
        Args:
            host (str): 主机地址
            port (int): 端口号
            buffer_size (int): 缓冲区大小
            max_connections (int): 最大连接数
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_connections = max_connections
        self.server_socket = None
        self.running = False
        self.clients = []

    def start(self):
        """启动服务器"""
        try:
            # 创建socket对象
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 设置地址重用
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 绑定地址
            self.server_socket.bind((self.host, self.port))
            
            # 开始监听
            self.server_socket.listen(self.max_connections)
            self.running = True
            
            print(f"服务器启动成功！")
            print(f"监听地址: {self.host}:{self.port}")
            print(f"最大连接数: {self.max_connections}")
            print("等待客户端连接...")
            
            # 接受客户端连接
            while self.running:
                try:
                    client_socket, client_addr = self.server_socket.accept()
                    print(f"新连接来自: {client_addr}")
                    
                    # 为每个客户端创建新线程
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_addr),
                        daemon=True
                    )
                    client_thread.start()
                    
                except OSError as e:
                    if self.running:
                        print(f"接受连接时出错: {e}")
                    break
                    
        except Exception as e:
            print(f"启动服务器失败: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket, client_addr):
        """
        处理客户端连接
        
        Args:
            client_socket: 客户端socket
            client_addr: 客户端地址
        """
        self.clients.append(client_socket)
        
        try:
            # 发送欢迎消息
            welcome_msg = f"欢迎连接到服务器！当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            while self.running:
                try:
                    # 接收客户端数据
                    data = client_socket.recv(self.buffer_size)
                    if not data:
                        break
                    
                    # 解码数据
                    message = data.decode('utf-8').strip()
                    print(f"<来自 {client_addr}: {message}>")
                    
                    # 处理特殊命令
                    if message.lower() == 'exit':
                        response = "再见！"
                        client_socket.send(response.encode('utf-8'))
                        break
                    elif message.lower() == 'time':
                        response = f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    elif message.lower() == 'help':
                        response = "可用命令: time, help, exit"
                    else:
                        # 回显消息
                        response = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
                    
                    # 发送响应
                    client_socket.send(response.encode('utf-8'))
                    
                except socket.error as e:
                    print(f"接收数据时出错: {e}")
                    break
                    
        except Exception as e:
            print(f"处理客户端 {client_addr} 时出错: {e}")
        finally:
            # 清理连接
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            print(f"客户端 {client_addr} 已断开连接")

    def stop(self):
        """停止服务器"""
        self.running = False
        
        # 关闭所有客户端连接
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # 关闭服务器socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("服务器已停止")

class SocketClient:
    """Socket客户端类"""
    
    def __init__(self, host="localhost", port=160214, buffer_size=1024):
        """
        初始化客户端
        
        Args:
            host (str): 服务器地址
            port (int): 服务器端口
            buffer_size (int): 缓冲区大小
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = None
        self.connected = False

    def connect(self):
        """连接到服务器"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            print(f"成功连接到服务器 {self.host}:{self.port}")
            
            # 接收欢迎消息
            welcome_msg = self.client_socket.recv(self.buffer_size)
            print(f"服务器: {welcome_msg.decode('utf-8')}")
            
            return True
            
        except Exception as e:
            print(f"连接服务器失败: {e}")
            return False

    def start_interactive_mode(self):
        """启动交互模式"""
        if not self.connected:
            print("请先连接到服务器")
            return
        
        print("\n=== 交互模式 ===")
        print("可用命令: time, help, exit")
        print("输入消息发送给服务器，输入 'exit' 退出\n")
        
        try:
            while self.connected:
                try:
                    # 获取用户输入
                    message = input("> ").strip()
                    
                    if not message:
                        continue
                    
                    # 发送消息
                    self.client_socket.send(message.encode('utf-8'))
                    
                    # 检查是否要退出
                    if message.lower() == 'exit':
                        break
                    
                    # 接收响应
                    response = self.client_socket.recv(self.buffer_size)
                    print(f"服务器: {response.decode('utf-8')}")
                    
                except KeyboardInterrupt:
                    print("\n用户中断，正在断开连接...")
                    break
                except socket.error as e:
                    print(f"通信错误: {e}")
                    break
                    
        except Exception as e:
            print(f"交互模式出错: {e}")
        finally:
            self.disconnect()

    def send_message(self, message):
        """
        发送单条消息
        
        Args:
            message (str): 要发送的消息
            
        Returns:
            str: 服务器响应
        """
        if not self.connected:
            return "未连接到服务器"
        
        try:
            self.client_socket.send(message.encode('utf-8'))
            response = self.client_socket.recv(self.buffer_size)
            return response.decode('utf-8')
        except Exception as e:
            return f"发送消息失败: {e}"

    def disconnect(self):
        """断开连接"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("已断开连接")

def run_server(host="localhost", port=160214):
    """运行服务器"""
    server = SocketServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n用户中断，正在停止服务器...")
        server.stop()

def run_client(host="localhost", port=160214):
    """运行客户端"""
    client = SocketClient(host, port)
    
    if client.connect():
        client.start_interactive_mode()

def test_connection(host="localhost", port=160214):
    """测试连接"""
    client = SocketClient(host, port)
    
    if client.connect():
        # 发送测试消息
        test_messages = ["hello", "time", "help", "exit"]
        
        for msg in test_messages:
            print(f"发送: {msg}")
            response = client.send_message(msg)
            print(f"响应: {response}")
            
            if msg.lower() == "exit":
                break
        
        client.disconnect()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Socket编程示例")
    parser.add_argument("mode", choices=["server", "client", "test"], 
                       help="运行模式: server(服务器), client(客户端), test(测试)")
    parser.add_argument("--host", default="localhost", help="主机地址 (默认: localhost)")
    parser.add_argument("--port", type=int, default=160214, help="端口号 (默认: 160214)")
    
    args = parser.parse_args()
    
    print(f"Socket编程示例 - {args.mode}模式")
    print("=" * 40)
    
    if args.mode == "server":
        run_server(args.host, args.port)
    elif args.mode == "client":
        run_client(args.host, args.port)
    elif args.mode == "test":
        test_connection(args.host, args.port)

if __name__ == "__main__":
    # 如果没有命令行参数，提供交互式选择
    if len(sys.argv) == 1:
        print("Socket编程示例")
        print("1. 启动服务器")
        print("2. 启动客户端")
        print("3. 测试连接")
        
        choice = input("请选择模式 (1/2/3): ").strip()
        
        if choice == "1":
            host = input("主机地址 (默认: localhost): ").strip() or "localhost"
            port = int(input("端口号 (默认: 160214): ").strip() or "160214")
            run_server(host, port)
        elif choice == "2":
            host = input("服务器地址 (默认: localhost): ").strip() or "localhost"
            port = int(input("端口号 (默认: 160214): ").strip() or "160214")
            run_client(host, port)
        elif choice == "3":
            host = input("服务器地址 (默认: localhost): ").strip() or "localhost"
            port = int(input("端口号 (默认: 160214): ").strip() or "160214")
            test_connection(host, port)
        else:
            print("无效选择")
    else:
        main()
    