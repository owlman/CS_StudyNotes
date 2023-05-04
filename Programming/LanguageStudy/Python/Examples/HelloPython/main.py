#! /usr/bin/env python
'''
    Created on 2020-3-1

    @author: lingjie
    @name : HelloPython
'''

def showStringOperator() :
    name = "lingjie"   # 存储一般的字符串数据
    I_am = "I'm "        # 存储带单引号的字符串数据
    # 储存包含多行内容的字符串数据
    other = '''
    age:  42
    job: writer
    '''
    message = I_am + name + other # 拼接字符串数据并存储
    
    print(message) # 输出变量 message 中存储的字符串数据
    print(message[0:11]) # 截取变量中的某一段字符串并输出

def showLIstOperator() :
    list_1 = [ # 将三个对象存储为一个列表类型的数据
        10,      # 第一个列表元素为数字类型的数据
        "string data", # 第二个列表元素为字符串类型的数据
        [1, 2, 3] # 第一个列表元素为列表类型的数据
    ]
    print(list_1) # 输出整个列表中的数据
    print(list_1[1]) # 用索引的方式输出指定的元素
    # 注意，列表元素的索引值是从 0 开始的，所以这里输出的是第二个元素
    list_1[0] = 100 # 修改指定的元素
    list_1.remove([1,2,3]) # 找到并删除列表中的第三个元素
    print(list_1) # 重新输出整个列表中的数据
    list_1.append([7, 8, 9])  # 在列表末尾重新添加元素
    print(list_1) # 重新输出整个列表中的数据

def showTupleOperator() :
    tuple_1 = ("abcd", 706, "xyy", 898, 5.2) # 一次性地存储一些数据
    print(tuple_1)          #  输出整个元组中的数据
    print(tuple_1[0])      # 用索引的方式输出指定的元素 
    print(tuple_1[1:3])   # 用索引区间的方式输出元组的某个子序列

def showSetsOperator() :
    set_1 = {18,19,18,20,21,20} # 如果我们存储的数组存在重复
    print(set_1)  # 读者就会看到相同的元素只会被保留一个

def showMapOperator() :
    map_1 = { # 将两个键值对元素存储为一个字典类型的数据
        "name" : "lingjie",  # name 是键，lingjie 是值
        "age" : "25"            # age 是键，25 是值
    }
    print(map_1) # 输出字典中的数据
    map_1["sex"] = "boy" # 添加一个键为 sex，值为 boy 的元素 
    print(map_1) # 重新输出字典中的数据

    # 字典删除数据时，可以使用 del 函数
    del map_1["age"] # 删除键为 age 的元素
    print(map_1) # 重新输出字典中的数据
    
class Book:
    help = '''
    这是一个类属性，用于提供当前类帮助信息。
    
    创建实例的方法：
        mybook = Book({
            "name" : "Python 快速入门",
            "author" : "lingjie",
            "pub" : "人民邮电出版社" 
        })
    修改书名的方法：
        mybook.updataName("Python 3 快速入门")
    销毁实例的方法：
        del mybook
    '''

    '''
      定义 Book 类的初始化方法，该方法需要定义以下两个参数：
        self：这是初始化方法必须要有的参数，
                用于指涉将被初始化的实例；
        bookdata：这是字典类型的数据对象，
                用于提供初始化时所要提供的数据；
    '''
    def __init__(self, bookdata):
        # 定义三个实例属性：
        self.name = bookdata["name"]
        self.author = bookdata["author"]
        self.pub = bookdata["pub"]
    
    '''
      定义 Book 类中用于修改书名的方法，它需要定义以下两个参数：
        self：用于指涉当前被称作的实例；
        newName：用于指定新书名的字符串对象；
    '''
    def updataName(self, newName) :
        self.name = newName

    '''
      定义 Book 类中用于销毁实例的方法，它需要定义以下参数：
        self：用于指涉当前被称作的实例；
    '''
    def __del__(self):
        print("delete ", self.name)        

def main():
    message = "This is an object-oriented,open-source programming language often used for rapid application development.Python's simple syntax amphasizes readability,reducing the cost of program mantenance, while its large library of functions and calls encourages reuse and extensibility."
    print("Hello Python! \n", message)
    
    showStringOperator()
    showLIstOperator()
    showTupleOperator()
    showSetsOperator()
    showMapOperator()
    
    # 下面演示使用自定义类型
    # 访问类属性的方法：
    print(Book.help)
    # 创建实例的方法：
    mybook = Book({
        "name" : "Python 快速入门",
        "author" : "lingjie",
        "pub" : "人民邮电出版社" 
    })
    # 修改书名的方法：
    mybook.updataName("Python 3 快速入门")
    # 销毁实例的方法：
    del mybook

    # 下面演示 if 语句的用法    
    exRate = -0.1404  # 现在汇率为负值。
    CNY = 200
    if (CNY < 0) :
        print('人民币的币值不能为负数！')
    elif (exRate < 0) :
        print('人民币对美元的汇率不能为负数！')
    else :
        USD = CNY * exRate
        print('换算的美元币值为：', USD)
        
    # 下面演示 for...in 语句的用法    
    list = range(0, 10)
    for i in list:
        print(i)

if (__name__ == "__main__"):
    main()

