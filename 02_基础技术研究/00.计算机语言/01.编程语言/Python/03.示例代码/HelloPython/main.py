#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Python基础语法示例
    
    Created on 2020-3-1
    Updated on 2025-11-26

    @author: lingjie
    @name : HelloPython
'''

def demonstrate_string_operations():
    """演示字符串操作"""
    print("=== 字符串操作 ===")
    
    # 基本字符串操作
    name = "lingjie"   # 存储一般的字符串数据
    I_am = "I'm "        # 存储带单引号的字符串数据
    
    # 多行字符串
    other = '''
    age:  42
    job: writer
    '''
    
    # 字符串拼接
    message = I_am + name + other
    print("完整消息:")
    print(message)
    
    # 字符串切片
    print(f"前11个字符: {message[0:11]}")
    
    # 字符串方法
    print(f"大写: {message.upper()}")
    print(f"小写: {message.lower()}")
    print(f"去除空白: {message.strip()}")
    print(f"长度: {len(message)}")
    
    # 字符串格式化
    formatted = f"姓名: {name}, 年龄: 42, 职业: writer"
    print(f"格式化字符串: {formatted}")
    
    # 字符串查找和替换
    if "lingjie" in message:
        print("消息中包含 'lingjie'")
    
    replaced = message.replace("lingjie", "张三")
    print(f"替换后: {replaced[:50]}...")

def demonstrate_list_operations():
    """演示列表操作"""
    print("\n=== 列表操作 ===")
    
    # 创建列表
    list_1 = [
        10,                    # 数字类型
        "string data",         # 字符串类型
        [1, 2, 3],            # 嵌套列表
        {"key": "value"},     # 字典
        (4, 5, 6)            # 元组
    ]
    
    print(f"原始列表: {list_1}")
    print(f"列表长度: {len(list_1)}")
    print(f"第二个元素: {list_1[1]}")  # 索引从0开始
    
    # 修改元素
    list_1[0] = 100
    print(f"修改第一个元素后: {list_1}")
    
    # 删除元素
    list_1.remove([1, 2, 3])
    print(f"删除嵌套列表后: {list_1}")
    
    # 添加元素
    list_1.append([7, 8, 9])
    print(f"添加新元素后: {list_1}")
    
    # 列表操作
    list_1.insert(1, "inserted")
    print(f"插入元素后: {list_1}")
    
    popped = list_1.pop()
    print(f"弹出的元素: {popped}")
    print(f"弹出后: {list_1}")
    
    # 列表切片
    print(f"前3个元素: {list_1[:3]}")
    print(f"后2个元素: {list_1[-2:]}")
    
    # 列表推导式
    squares = [x**2 for x in range(10)]
    print(f"平方列表: {squares}")

def demonstrate_tuple_operations():
    """演示元组操作"""
    print("\n=== 元组操作 ===")
    
    # 创建元组
    tuple_1 = ("abcd", 706, "xyy", 898, 5.2)
    print(f"元组: {tuple_1}")
    print(f"第一个元素: {tuple_1[0]}")
    print(f"切片 [1:3]: {tuple_1[1:3]}")
    
    # 元组不可变
    try:
        tuple_1[0] = "changed"
    except TypeError as e:
        print(f"元组不可变错误: {e}")
    
    # 元组解包
    a, b, c, d, e = tuple_1
    print(f"解包后: a={a}, b={b}, c={c}")
    
    # 命名元组
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print(f"命名元组: {p}, x={p.x}, y={p.y}")

def demonstrate_set_operations():
    """演示集合操作"""
    print("\n=== 集合操作 ===")
    
    # 创建集合（自动去重）
    set_1 = {18, 19, 18, 20, 21, 20}
    print(f"自动去重后的集合: {set_1}")
    
    # 集合操作
    set_2 = {20, 21, 22, 23}
    print(f"另一个集合: {set_2}")
    
    print(f"并集: {set_1 | set_2}")
    print(f"交集: {set_1 & set_2}")
    print(f"差集: {set_1 - set_2}")
    print(f"对称差集: {set_1 ^ set_2}")
    
    # 集合方法
    set_1.add(25)
    print(f"添加元素后: {set_1}")
    
    set_1.discard(18)
    print(f"删除元素后: {set_1}")

def demonstrate_dict_operations():
    """演示字典操作"""
    print("\n=== 字典操作 ===")
    
    # 创建字典
    map_1 = {
        "name": "lingjie",
        "age": "25"
    }
    print(f"原始字典: {map_1}")
    
    # 添加元素
    map_1["sex"] = "boy"
    print(f"添加元素后: {map_1}")
    
    # 访问元素
    print(f"姓名: {map_1.get('name', '未知')}")
    print(f"城市: {map_1.get('city', '北京')}")  # 默认值
    
    # 删除元素
    del map_1["age"]
    print(f"删除age后: {map_1}")
    
    # 字典方法
    print(f"所有键: {list(map_1.keys())}")
    print(f"所有值: {list(map_1.values())}")
    print(f"所有键值对: {list(map_1.items())}")
    
    # 字典推导式
    squares_dict = {x: x**2 for x in range(5)}
    print(f"平方字典: {squares_dict}")

class Book:
    """书籍类"""
    
    # 类属性
    help_text = '''
    这是一个书籍类，用于演示面向对象编程。
    
    创建实例的方法：
        mybook = Book({
            "name": "Python 快速入门",
            "author": "lingjie",
            "pub": "人民邮电出版社" 
        })
    
    修改书名的方法：
        mybook.update_name("Python 3 快速入门")
    
    获取书籍信息的方法：
        mybook.get_info()
    '''

    def __init__(self, book_data):
        """
        初始化书籍对象
        
        Args:
            book_data (dict): 包含书籍信息的字典
        """
        self.name = book_data["name"]
        self.author = book_data["author"]
        self.pub = book_data["pub"]
        self.created_at = "2025-11-26"  # 添加创建时间
    
    def update_name(self, new_name):
        """
        更新书名
        
        Args:
            new_name (str): 新书名
        """
        old_name = self.name
        self.name = new_name
        print(f"书名已从 '{old_name}' 更新为 '{new_name}'")
    
    def get_info(self):
        """获取书籍信息"""
        info = {
            "书名": self.name,
            "作者": self.author,
            "出版社": self.pub,
            "创建时间": self.created_at
        }
        return info
    
    def __str__(self):
        """字符串表示"""
        return f"《{self.name}》- {self.author} ({self.pub})"
    
    def __del__(self):
        """析构方法"""
        print(f"销毁书籍: {self.name}")

def demonstrate_class_operations():
    """演示类操作"""
    print("\n=== 类操作 ===")
    
    # 访问类属性
    print(Book.help_text)
    
    # 创建实例
    book_data = {
        "name": "Python 快速入门",
        "author": "lingjie",
        "pub": "人民邮电出版社"
    }
    
    mybook = Book(book_data)
    print(f"创建的书籍: {mybook}")
    
    # 修改书名
    mybook.update_name("Python 3 快速入门")
    
    # 获取信息
    info = mybook.get_info()
    print("书籍详细信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 销毁实例（显式调用）
    del mybook

def demonstrate_control_flow():
    """演示控制流"""
    print("\n=== 控制流 ===")
    
    # if-elif-else语句
    exchange_rate = -0.1404  # 汇率为负值
    cny_amount = 200
    
    if cny_amount < 0:
        print('人民币的币值不能为负数！')
    elif exchange_rate < 0:
        print('人民币对美元的汇率不能为负数！')
    else:
        usd_amount = cny_amount * exchange_rate
        print(f'换算的美元币值为：{usd_amount:.2f}')
    
    # for循环
    print("\nfor循环示例:")
    for i in range(10):
        if i % 2 == 0:
            print(f"{i} 是偶数")
        else:
            print(f"{i} 是奇数")
    
    # while循环
    print("\nwhile循环示例:")
    count = 0
    while count < 5:
        print(f"计数: {count}")
        count += 1
    
    # 列表推导式与条件
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"偶数的平方: {even_squares}")

def demonstrate_exception_handling():
    """演示异常处理"""
    print("\n=== 异常处理 ===")
    
    # 基本异常处理
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("捕获到除零错误")
    except Exception as e:
        print(f"捕获到其他错误: {e}")
    else:
        print("没有发生错误")
    finally:
        print("无论是否出错都会执行")
    
    # 自定义异常
    class CustomError(Exception):
        pass
    
    try:
        raise CustomError("这是一个自定义错误")
    except CustomError as e:
        print(f"捕获自定义错误: {e}")

def main():
    """主函数"""
    print("Hello Python!")
    print("=" * 50)
    
    # Python描述
    message = ("Python是一种面向对象、开源的编程语言，常用于快速应用开发。"
              "Python的简洁语法强调可读性，降低了程序维护成本，"
              "其丰富的函数库和调用鼓励代码重用和扩展性。")
    print(message)
    
    # 运行各种演示
    demonstrate_string_operations()
    demonstrate_list_operations()
    demonstrate_tuple_operations()
    demonstrate_set_operations()
    demonstrate_dict_operations()
    demonstrate_class_operations()
    demonstrate_control_flow()
    demonstrate_exception_handling()
    
    print("\n" + "=" * 50)
    print("演示完成！")

if __name__ == "__main__":
    main()

