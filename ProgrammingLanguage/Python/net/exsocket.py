#! /bin/env python
# -*- coding: UTF-8 -*-
'''
    Created on 2009-9-4

    @author: lingjie
    @name : example_socket_proc
'''

from socket import *
from time import ctime

#服务器端
def serverside(host="", port=160214, bufsize=1024):
    addr = (host, port)
    servsocket = socket(AF_INET, SOCK_STREAM)
    servsocket.bind(addr)
    servsocket.listen(5)
    
    while True:
        print "waiting for connection..."
        clisock, addr = servsocket.accept()
        print "...connected from:", addr
        
        while True:
            try:
                data = servsocket.recv(bufsize)
                print "<", data
                clisock.send('[%s] %s' % (ctime(), data)) 
            except:
                print "disconnect from:", addr
                clisock.close() 
                break
    
    servsocket.close()

#客户端    
def cliectside(host="localhost", port=160214, bufsize=1024):
    addr = (host, port)
    clisocket = socket(AF_INET, SOCK_STREAM)
    clisocket.connect(addr)
    try:
        while True:
            data = raw_input(">")
            if data == "close":
                break
            if not data:
                continue
            clisocket.send(data)
            data = clisocket.recv(bufsize)
            print data
    except:
        clisocket.close()
    