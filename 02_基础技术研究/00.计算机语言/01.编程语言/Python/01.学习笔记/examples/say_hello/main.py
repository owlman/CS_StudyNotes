#! /usr/bin/env python
'''
    Simple example to say hello
    
    Author: lingjie
    Created on: 2024-06-15
    '''

author_name = "owlman"  # global variable
def say_hello(name: str) -> None:
    '''
        Say hello by name.
     
        Args:
            name: name to greet
    '''
    print("Hello World! My name is", name)
    message = "\nThis is an object-oriented,open-source programming language often used for rapid application development.Python's simple syntax amphasizes readability,reducing the cost of program mantenance, while its large library of functions and calls encourages reuse and extensibility."
    print(message)
    print("") # print a blank line

def say_hello_to_me() -> None:
    '''
        Say hello to myself.
    '''
    author_name = "lingjie" # local variable
    say_hello(author_name)

if __name__ == "__main__":
    say_hello(author_name) 
    say_hello_to_me()      
