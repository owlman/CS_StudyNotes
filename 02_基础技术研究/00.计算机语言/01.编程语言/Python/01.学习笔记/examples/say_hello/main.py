#! /usr/bin/env python
'''
    Simple example to say hello
    
    Author: lingjie
    Created on: 2024-06-15
    '''

def say_hello(name: str) -> None:
    '''
        Say hello by name.
     
        Args:
            name: name to greet
    '''
    print("Hello World! My name is", name)

if __name__ == "__main__":
    author_name = "lingjie"    
    say_hello(author_name)
