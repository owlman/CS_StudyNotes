#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    平台检测工具
    
    Created on 2016-5-2
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   check_platform
'''

import os
import platform
import sys
import subprocess
from pathlib import Path

def get_system_info():
    """获取详细的系统信息"""
    print("========== 系统信息 ==========")
    
    # 操作系统信息
    print(f"操作系统: {platform.system()}")
    print(f"系统版本: {platform.release()}")
    print(f"系统架构: {platform.machine()}")
    print(f"处理器架构: {platform.processor()}")
    print(f"平台详情: {platform.platform()}")
    print(f"架构信息: {platform.architecture()}")
    
    # Python信息
    print(f"\nPython版本: {platform.python_version()}")
    print(f"Python实现: {platform.python_implementation()}")
    print(f"Python编译器: {platform.python_compiler()}")
    print(f"Python构建: {platform.python_build()}")
    
    # 环境变量
    print(f"\nPython路径: {sys.executable}")
    print(f"Python版本详情: {sys.version}")
    print(f"平台: {sys.platform}")
    
    # 当前目录信息
    current_dir = Path.cwd()
    print(f"\n当前目录: {current_dir}")
    print(f"用户主目录: {Path.home()}")

def get_environment_variables():
    """获取重要环境变量"""
    print("\n========== 重要环境变量 ==========")
    
    important_vars = [
        'PATH',
        'PYTHONPATH',
        'HOME' if platform.system() != 'Windows' else 'USERPROFILE',
        'TEMP' if platform.system() == 'Windows' else 'TMPDIR',
        'COMPUTERNAME' if platform.system() == 'Windows' else 'HOSTNAME',
        'USERNAME' if platform.system() == 'Windows' else 'USER'
    ]
    
    for var in important_vars:
        value = os.environ.get(var, '未设置')
        if var == 'PATH' and len(value) > 100:
            # 对PATH进行截断显示
            value = value[:100] + '... (截断)'
        print(f"{var}: {value}")

def get_disk_info():
    """获取磁盘信息"""
    print("\n========== 磁盘信息 ==========")
    
    try:
        if platform.system() == 'Windows':
            # Windows系统
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            caption = parts[0]
                            free_space = int(parts[1]) if parts[1].isdigit() else 0
                            total_space = int(parts[2]) if parts[2].isdigit() else 0
                            
                            free_gb = free_space / (1024**3)
                            total_gb = total_space / (1024**3)
                            
                            print(f"驱动器 {caption}: 总空间 {total_gb:.2f}GB, 可用空间 {free_gb:.2f}GB")
        else:
            # Linux/Unix系统
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
    except Exception as e:
        print(f"获取磁盘信息失败: {e}")

def get_network_info():
    """获取网络信息"""
    print("\n========== 网络信息 ==========")
    
    try:
        import socket
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        print(f"主机名: {hostname}")
        print(f"IP地址: {ip_address}")
        
        # 获取所有网络接口
        if platform.system() != 'Windows':
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                print("\n网络接口详情:")
                print(result.stdout)
        else:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            if result.returncode == 0:
                print("\n网络配置详情:")
                print(result.stdout)
                
    except Exception as e:
        print(f"获取网络信息失败: {e}")

def execute_platform_specific_tasks():
    """执行平台特定任务"""
    system_type = platform.system()
    
    print(f"\n========== {system_type} 特定任务 ==========")
    
    if system_type == "Windows":
        print("执行Windows特定任务...")
        try:
            # 获取Windows版本信息
            result = subprocess.run(['ver'], shell=True, capture_output=True, text=True)
            print(f"Windows版本: {result.stdout.strip()}")
            
            # 获取环境变量
            print("\nWindows环境变量示例:")
            print(f"Program Files: {os.environ.get('ProgramFiles', '未设置')}")
            print(f"SystemRoot: {os.environ.get('SystemRoot', '未设置')}")
            
        except Exception as e:
            print(f"Windows任务执行失败: {e}")
            
    elif system_type == "Linux":
        print("执行Linux特定任务...")
        try:
            # 获取Linux发行版信息
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    print("\nLinux发行版信息:")
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            print(line.strip())
            
            # 获取内存信息
            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r') as f:
                    print("\n内存信息:")
                    for i, line in enumerate(f):
                        if i >= 5:  # 只显示前5行
                            break
                        print(line.strip())
                        
        except Exception as e:
            print(f"Linux任务执行失败: {e}")
            
    elif system_type == "Darwin":  # macOS
        print("执行macOS特定任务...")
        try:
            # 获取macOS版本
            result = subprocess.run(['sw_vers'], capture_output=True, text=True)
            if result.returncode == 0:
                print("\nmacOS版本信息:")
                print(result.stdout)
                
        except Exception as e:
            print(f"macOS任务执行失败: {e}")
    else:
        print(f"其他系统: {system_type}")
        print("没有针对此系统的特定任务")

def test_python_features():
    """测试Python特性"""
    print("\n========== Python特性测试 ==========")
    
    # 测试编码
    test_string = "测试中文字符串"
    print(f"字符串编码测试: {test_string}")
    print(f"字符串编码: {test_string.encode('utf-8')}")
    
    # 测试路径操作
    test_path = Path("/tmp/test_file.txt")
    print(f"\n路径操作测试:")
    print(f"路径对象: {test_path}")
    print(f"路径名称: {test_path.name}")
    print(f"路径后缀: {test_path.suffix}")
    print(f"父目录: {test_path.parent}")
    
    # 测试系统调用
    print(f"\n系统调用测试:")
    print(f"当前进程ID: {os.getpid()}")
    print(f"父进程ID: {os.getppid()}")

def main():
    """主函数"""
    print("Python平台检测工具")
    print("=" * 50)
    
    try:
        # 获取系统信息
        get_system_info()
        
        # 获取环境变量
        get_environment_variables()
        
        # 执行平台特定任务
        execute_platform_specific_tasks()
        
        # 获取磁盘信息
        get_disk_info()
        
        # 获取网络信息
        get_network_info()
        
        # 测试Python特性
        test_python_features()
        
        print("\n" + "=" * 50)
        print("平台检测完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
