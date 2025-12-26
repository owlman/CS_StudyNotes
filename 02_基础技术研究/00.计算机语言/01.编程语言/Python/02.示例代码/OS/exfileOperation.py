#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    文件操作示例
    
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   example_file_operations
'''

import os
import sys
import shutil
import pathlib
import tempfile
import subprocess
from pathlib import Path

class FileManager:
    """文件管理器类"""
    
    def __init__(self, base_dir=None):
        """
        初始化文件管理器
        
        Args:
            base_dir (str): 基础目录，默认为脚本所在目录
        """
        self.base_dir = Path(base_dir) if base_dir else Path(sys.path[0]).resolve()
        print(f"文件管理器初始化，基础目录: {self.base_dir}")
    
    def show_directory_info(self):
        """显示目录信息"""
        print("\n=== 目录信息 ===")
        print(f"当前工作目录: {Path.cwd()}")
        print(f"脚本所在目录: {self.base_dir}")
        print(f"用户主目录: {Path.home()}")
        
        # 列出基础目录内容
        if self.base_dir.exists():
            print(f"\n基础目录内容:")
            try:
                items = list(self.base_dir.iterdir())
                for item in sorted(items):
                    if item.is_file():
                        print(f"  文件: {item.name} ({item.stat().st_size} bytes)")
                    elif item.is_dir():
                        print(f"  目录: {item.name}/")
            except PermissionError:
                print(f"  权限不足，无法读取目录内容")
    
    def create_directory_structure(self):
        """创建目录结构"""
        print("\n=== 创建目录结构 ===")
        
        # 创建主目录
        example_dir = self.base_dir / "example"
        try:
            example_dir.mkdir(exist_ok=True)
            print(f"创建目录: {example_dir}")
        except Exception as e:
            print(f"创建目录失败: {e}")
            return False
        
        # 创建子目录
        sub_dir = example_dir / "sub"
        try:
            sub_dir.mkdir(exist_ok=True)
            print(f"创建子目录: {sub_dir}")
        except Exception as e:
            print(f"创建子目录失败: {e}")
            return False
        
        # 创建更多子目录用于演示
        demo_dirs = ["data", "logs", "temp"]
        for dir_name in demo_dirs:
            dir_path = example_dir / dir_name
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"创建目录: {dir_path}")
            except Exception as e:
                print(f"创建目录 {dir_name} 失败: {e}")
        
        return True
    
    def create_sample_files(self):
        """创建示例文件"""
        print("\n=== 创建示例文件 ===")
        
        example_dir = self.base_dir / "example"
        
        # 创建hello.py文件
        hello_file = example_dir / "hello.py"
        try:
            hello_content = '''#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    示例Python文件
"""

def main():
    print("Hello, World! from example file")
    print("这是一个自动生成的示例文件")

if __name__ == "__main__":
    main()
'''
            hello_file.write_text(hello_content, encoding='utf-8')
            print(f"创建文件: {hello_file}")
        except Exception as e:
            print(f"创建文件失败: {e}")
            return False
        
        # 创建配置文件
        config_file = example_dir / "config.ini"
        try:
            config_content = '''[database]
host = localhost
port = 3306
username = admin
password = secret

[logging]
level = INFO
file = app.log
max_size = 10MB
'''
            config_file.write_text(config_content, encoding='utf-8')
            print(f"创建文件: {config_file}")
        except Exception as e:
            print(f"创建配置文件失败: {e}")
        
        # 创建数据文件
        data_file = example_dir / "data" / "sample.txt"
        try:
            data_content = '''这是示例数据文件
包含多行文本内容
用于演示文件操作

第1行: Hello
第2行: World
第3行: Python
'''
            data_file.write_text(data_content, encoding='utf-8')
            print(f"创建文件: {data_file}")
        except Exception as e:
            print(f"创建数据文件失败: {e}")
        
        return True
    
    def read_and_display_files(self):
        """读取并显示文件内容"""
        print("\n=== 读取文件内容 ===")
        
        example_dir = self.base_dir / "example"
        
        # 读取hello.py
        hello_file = example_dir / "hello.py"
        if hello_file.exists():
            try:
                content = hello_file.read_text(encoding='utf-8')
                print(f"\n{hello_file.name} 内容:")
                print("-" * 30)
                print(content)
                print("-" * 30)
            except Exception as e:
                print(f"读取文件失败: {e}")
        
        # 读取配置文件
        config_file = example_dir / "config.ini"
        if config_file.exists():
            try:
                content = config_file.read_text(encoding='utf-8')
                print(f"\n{config_file.name} 内容:")
                print("-" * 30)
                print(content)
                print("-" * 30)
            except Exception as e:
                print(f"读取配置文件失败: {e}")
    
    def execute_python_file(self):
        """执行Python文件"""
        print("\n=== 执行Python文件 ===")
        
        hello_file = self.base_dir / "example" / "hello.py"
        if hello_file.exists():
            try:
                print(f"执行文件: {hello_file}")
                result = subprocess.run(
                    [sys.executable, str(hello_file)], 
                    capture_output=True, 
                    text=True,
                    cwd=str(hello_file.parent)
                )
                
                if result.returncode == 0:
                    print("执行输出:")
                    print(result.stdout)
                else:
                    print(f"执行失败，返回码: {result.returncode}")
                    if result.stderr:
                        print(f"错误信息: {result.stderr}")
                        
            except Exception as e:
                print(f"执行文件失败: {e}")
    
    def copy_and_move_operations(self):
        """复制和移动操作"""
        print("\n=== 复制和移动操作 ===")
        
        example_dir = self.base_dir / "example"
        temp_dir = self.base_dir / "temp"
        
        try:
            # 复制整个目录
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            shutil.copytree(example_dir, temp_dir)
            print(f"复制目录: {example_dir} -> {temp_dir}")
            
            # 复制单个文件
            backup_file = example_dir / "hello_backup.py"
            hello_file = example_dir / "hello.py"
            if hello_file.exists():
                shutil.copy2(hello_file, backup_file)
                print(f"复制文件: {hello_file} -> {backup_file}")
            
            # 移动文件
            moved_file = example_dir / "data" / "moved_sample.txt"
            original_file = example_dir / "data" / "sample.txt"
            if original_file.exists():
                shutil.move(str(original_file), str(moved_file))
                print(f"移动文件: {original_file} -> {moved_file}")
                
        except Exception as e:
            print(f"复制/移动操作失败: {e}")
    
    def file_search_operations(self):
        """文件搜索操作"""
        print("\n=== 文件搜索操作 ===")
        
        example_dir = self.base_dir / "example"
        
        # 搜索所有.py文件
        print("搜索Python文件:")
        try:
            py_files = list(example_dir.rglob("*.py"))
            for file_path in py_files:
                size = file_path.stat().st_size
                print(f"  {file_path.relative_to(self.base_dir)} ({size} bytes)")
        except Exception as e:
            print(f"搜索Python文件失败: {e}")
        
        # 搜索包含特定内容的文件
        print("\n搜索包含 'Hello' 的文件:")
        try:
            for file_path in example_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if "Hello" in content:
                            print(f"  {file_path.relative_to(self.base_dir)}")
                    except:
                        pass  # 忽略无法读取的文件
        except Exception as e:
            print(f"搜索文件内容失败: {e}")
    
    def cleanup_operations(self):
        """清理操作"""
        print("\n=== 清理操作 ===")
        
        # 删除临时目录
        temp_dir = self.base_dir / "temp"
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
                print(f"删除临时目录: {temp_dir}")
            except Exception as e:
                print(f"删除临时目录失败: {e}")
        
        # 显示清理后的目录结构
        example_dir = self.base_dir / "example"
        if example_dir.exists():
            print(f"\n清理后的目录结构:")
            try:
                for item in example_dir.rglob("*"):
                    if item.is_file():
                        print(f"  文件: {item.relative_to(self.base_dir)}")
                    elif item.is_dir():
                        print(f"  目录: {item.relative_to(self.base_dir)}/")
            except Exception as e:
                print(f"显示目录结构失败: {e}")
    
    def demonstrate_path_operations(self):
        """演示路径操作"""
        print("\n=== 路径操作演示 ===")
        
        # 创建路径对象
        test_path = Path(self.base_dir) / "example" / "sub" / "test.txt"
        
        print(f"路径对象: {test_path}")
        print(f"路径名称: {test_path.name}")
        print(f"路径后缀: {test_path.suffix}")
        print(f"路径主干: {test_path.stem}")
        print(f"父目录: {test_path.parent}")
        print(f"父目录的父目录: {test_path.parent.parent}")
        print(f"是否为绝对路径: {test_path.is_absolute()}")
        print(f"解析为绝对路径: {test_path.resolve()}")
        
        # 路径操作
        print(f"\n路径操作:")
        print(f"是否存在: {test_path.exists()}")
        print(f"是否为文件: {test_path.is_file()}")
        print(f"是否为目录: {test_path.is_dir()}")
        
        # 路径拼接
        base = Path("/home/user")
        new_path = base / "documents" / "file.txt"
        print(f"\n路径拼接: {new_path}")
        
        # 路径分解
        print(f"路径分解: {list(test_path.parts)}")

def main():
    """主函数"""
    print("Python文件操作示例")
    print("=" * 50)
    
    try:
        # 创建文件管理器
        file_manager = FileManager()
        
        # 显示目录信息
        file_manager.show_directory_info()
        
        # 创建目录结构
        if file_manager.create_directory_structure():
            # 创建示例文件
            file_manager.create_sample_files()
            
            # 读取并显示文件内容
            file_manager.read_and_display_files()
            
            # 执行Python文件
            file_manager.execute_python_file()
            
            # 复制和移动操作
            file_manager.copy_and_move_operations()
            
            # 文件搜索操作
            file_manager.file_search_operations()
            
            # 路径操作演示
            file_manager.demonstrate_path_operations()
            
            # 清理操作
            file_manager.cleanup_operations()
        
        print("\n" + "=" * 50)
        print("文件操作示例完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
