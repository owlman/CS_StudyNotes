#! /usr/bin/env python
'''
    Created on 2020-3-1

    @author: lingjie
    @name : Hello Python
'''

auther_name = "lingjie"

def say_hello(name):
    '''this is a function to say hello.'''
    print("Hello World! My name is", name)

    # 定义一个包含较长文本的变量 message
    message = "\nThis is an object-oriented,open-source programming language often used for rapid application development.Python's simple syntax amphasizes readability,reducing the cost of program mantenance, while its large library of functions and calls encourages reuse and extensibility."
    print(message)

    
def another_name():
    '''this is another function.'''
    # 在函数内部重新定义一个名为 auther_name 的变量
    auther_name = "owlman"
    # 此时 auther_name 变量的值为 "owlman" 
    say_hello(auther_name)

if __name__ == "__main__":
    # 此时 auther_name 变量的值为 "lingjie"
    say_hello(auther_name)
    print()
    another_name()
