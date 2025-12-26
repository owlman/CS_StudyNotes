#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Created on 2014-11-20
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   example_file_proc
'''

import os
import sys

def one_time_reading(filepath):
    """一次性读取整个文件内容"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件 {filepath} 不存在")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
            return content
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None
        
def fixed_bytes_reading(filepath, chunk_size=8):
    """按固定字节数读取文件"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件 {filepath} 不存在")
            
        content = ""
        with open(filepath, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                content += chunk
        print(content)
        return content
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def read_by_line(filepath): 
    """逐行读取文件"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件 {filepath} 不存在")
            
        content = ""
        with open(filepath, "r", encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                content += line
        print(content)
        return content
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def read_all_lines(filepath):
    """一次性读取所有行"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件 {filepath} 不存在")
            
        with open(filepath, "r", encoding='utf-8') as f:
            txt_list = f.readlines()

        for line in txt_list:
            print(line, end='')
        return txt_list
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def write_file(filepath, content, mode='w'):
    """写入文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)
        print(f"成功写入文件: {filepath}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

def append_file(filepath, content):
    """追加内容到文件"""
    write_file(filepath, content, 'a')

if __name__ == "__main__":
    # 示例用法
    test_file = "test_data.txt"
    
    # 创建测试文件
    write_file(test_file, "这是测试文件\n第一行\n第二行\n第三行")
    
    # 测试各种读取方法
    print("=== 一次性读取 ===")
    one_time_reading(test_file)
    
    print("\n=== 按字节读取 ===")
    fixed_bytes_reading(test_file, 5)
    
    print("\n=== 逐行读取 ===")
    read_by_line(test_file)
    
    print("\n=== 读取所有行 ===")
    read_all_lines(test_file)
    
    # 清理测试文件
    try:
        os.remove(test_file)
    except:
        pass

        
     