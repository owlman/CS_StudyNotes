#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    简单的Hello World程序
    
    Updated on 2025-11-26
"""

import sys
import os
from datetime import datetime

def main():
    """主函数"""
    print("Hello, World!")
    
    # 显示更多系统信息
    print(f"\n=== 系统信息 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"当前目录: {os.getcwd()}")
    print(f"脚本路径: {__file__}")
    
    # 显示命令行参数
    if len(sys.argv) > 1:
        print(f"\n=== 命令行参数 ===")
        for i, arg in enumerate(sys.argv):
            print(f"参数 {i}: {arg}")
    else:
        print(f"\n用法: python {os.path.basename(__file__)} [参数1] [参数2] ...")

if __name__ == "__main__":
    main()