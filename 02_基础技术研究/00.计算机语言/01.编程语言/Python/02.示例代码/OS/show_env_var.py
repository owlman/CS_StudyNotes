#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    环境变量查看工具
    
    Created on 2016-6-19
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   show_env_var
'''

import os
import sys
import platform
from pathlib import Path

def display_platform_info():
    """显示平台信息"""
    print("========== 平台信息 ==========")
    print(f"操作系统: {platform.system()}")
    print(f"系统版本: {platform.release()}")
    print(f"系统架构: {platform.machine()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"Python路径: {sys.executable}")
    print(f"当前工作目录: {Path.cwd()}")
    print(f"用户主目录: {Path.home()}")

def display_environment_variables():
    """显示环境变量"""
    print("\n========== 环境变量 ==========")
    
    # 获取所有环境变量
    env_vars = os.environ
    
    # 按名称排序
    sorted_vars = sorted(env_vars.items())
    
    # 分类显示重要环境变量
    important_vars = {
        'PATH': '系统可执行文件路径',
        'PYTHONPATH': 'Python模块搜索路径',
        'HOME' if platform.system() != 'Windows' else 'USERPROFILE': '用户主目录',
        'TEMP' if platform.system() == 'Windows' else 'TMPDIR': '临时文件目录',
        'COMPUTERNAME' if platform.system() == 'Windows' else 'HOSTNAME': '主机名',
        'USERNAME' if platform.system() == 'Windows' else 'USER': '用户名',
        'SHELL': 'Shell程序',
        'LANG': '语言设置',
        'LC_ALL': '本地化设置'
    }
    
    # 显示重要环境变量
    print("重要环境变量:")
    for var_name, description in important_vars.items():
        value = env_vars.get(var_name, '未设置')
        if var_name == 'PATH' and len(value) > 100:
            # 对PATH进行适当截断
            value = value[:100] + '... (截断显示)'
        print(f"  {var_name}: {value}")
        print(f"    描述: {description}")
    
    # 显示所有环境变量
    print(f"\n所有环境变量 (共 {len(sorted_vars)} 个):")
    print("-" * 60)
    
    for var_name, var_value in sorted_vars:
        # 对过长的值进行截断
        if len(var_value) > 80:
            display_value = var_value[:80] + '... (截断)'
        else:
            display_value = var_value
        
        print(f"[{var_name}]: {display_value}")

def analyze_path_variable():
    """分析PATH环境变量"""
    print("\n========== PATH 变量分析 ==========")
    
    path_var = os.environ.get('PATH', '')
    if not path_var:
        print("PATH 环境变量未设置")
        return
    
    # 分割路径
    path_separator = ';' if platform.system() == 'Windows' else ':'
    paths = [p.strip() for p in path_var.split(path_separator) if p.strip()]
    
    print(f"PATH 包含 {len(paths)} 个路径:")
    
    # 检查每个路径
    existing_paths = []
    non_existing_paths = []
    
    for i, path in enumerate(paths, 1):
        exists = os.path.exists(path)
        print(f"  {i:2d}. {path}")
        print(f"      存在: {'是' if exists else '否'}")
        
        if exists:
            existing_paths.append(path)
            # 显示目录下的文件数量
            try:
                file_count = len([f for f in os.listdir(path) 
                                if os.path.isfile(os.path.join(path, f))])
                print(f"      文件数: {file_count}")
            except PermissionError:
                print(f"      文件数: 权限不足")
        else:
            non_existing_paths.append(path)
    
    # 统计信息
    print(f"\nPATH 统计:")
    print(f"  总路径数: {len(paths)}")
    print(f"  存在的路径: {len(existing_paths)}")
    print(f"  不存在的路径: {len(non_existing_paths)}")
    
    if non_existing_paths:
        print(f"\n不存在的路径:")
        for path in non_existing_paths:
            print(f"  - {path}")

def search_python_executables():
    """搜索Python可执行文件"""
    print("\n========== Python 可执行文件搜索 ==========")
    
    path_var = os.environ.get('PATH', '')
    if not path_var:
        print("PATH 环境变量未设置，无法搜索")
        return
    
    path_separator = ';' if platform.system() == 'Windows' else ':'
    paths = [p.strip() for p in path_var.split(path_separator) if p.strip()]
    
    python_executables = []
    
    for path in paths:
        if os.path.exists(path):
            try:
                files = os.listdir(path)
                for file in files:
                    file_lower = file.lower()
                    # 查找Python相关的可执行文件
                    if (file_lower.startswith('python') or 
                        file_lower.startswith('python3') or
                        file_lower == 'py.exe' or
                        file_lower == 'pyw.exe'):
                        
                        full_path = os.path.join(path, file)
                        python_executables.append(full_path)
            except PermissionError:
                continue
    
    if python_executables:
        print(f"找到 {len(python_executables)} 个Python可执行文件:")
        for exe in sorted(python_executables):
            print(f"  {exe}")
    else:
        print("在PATH中未找到Python可执行文件")

def display_environment_summary():
    """显示环境变量摘要"""
    print("\n========== 环境变量摘要 ==========")
    
    env_vars = os.environ
    
    # 统计信息
    total_vars = len(env_vars)
    total_length = sum(len(key) + len(value) for key, value in env_vars.items())
    
    print(f"环境变量总数: {total_vars}")
    print(f"总字符数: {total_length}")
    print(f"平均长度: {total_length / total_vars:.1f}")
    
    # 按类别统计
    categories = {
        'Python相关': 0,
        '系统路径': 0,
        '用户信息': 0,
        '程序配置': 0,
        '其他': 0
    }
    
    python_keywords = ['python', 'pip', 'conda', 'virtualenv']
    path_keywords = ['path', 'home', 'temp', 'tmp', 'user', 'profile']
    user_keywords = ['user', 'username', 'home', 'profile']
    program_keywords = ['program', 'app', 'software', 'system']
    
    for var_name in env_vars:
        var_lower = var_name.lower()
        
        if any(keyword in var_lower for keyword in python_keywords):
            categories['Python相关'] += 1
        elif any(keyword in var_lower for keyword in path_keywords):
            categories['系统路径'] += 1
        elif any(keyword in var_lower for keyword in user_keywords):
            categories['用户信息'] += 1
        elif any(keyword in var_lower for keyword in program_keywords):
            categories['程序配置'] += 1
        else:
            categories['其他'] += 1
    
    print("\n环境变量分类:")
    for category, count in categories.items():
        print(f"  {category}: {count}")

def export_environment_info():
    """导出环境信息到文件"""
    print("\n========== 导出环境信息 ==========")
    
    try:
        output_file = "environment_info.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("环境信息报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"生成时间: {os.popen('date /t && time /t' if platform.system() == 'Windows' else 'date').read().strip()}\n")
            f.write(f"操作系统: {platform.system()} {platform.release()}\n")
            f.write(f"Python版本: {platform.python_version()}\n")
            f.write(f"当前目录: {Path.cwd()}\n\n")
            
            f.write("环境变量:\n")
            f.write("-" * 50 + "\n")
            
            for var_name, var_value in sorted(os.environ.items()):
                f.write(f"[{var_name}]: {var_value}\n")
        
        print(f"环境信息已导出到: {output_file}")
        
    except Exception as e:
        print(f"导出环境信息失败: {e}")

def main():
    """主函数"""
    print("环境变量查看工具")
    print("=" * 50)
    
    try:
        # 显示平台信息
        display_platform_info()
        
        # 显示环境变量
        display_environment_variables()
        
        # 分析PATH变量
        analyze_path_variable()
        
        # 搜索Python可执行文件
        search_python_executables()
        
        # 显示环境变量摘要
        display_environment_summary()
        
        # 导出环境信息
        export_environment_info()
        
        print("\n" + "=" * 50)
        print("环境变量分析完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()