#! /bin/env python
# -*- coding: UTF-8 -*-
'''
    Created on 2014-11-20
    
    @author: lingjie
    @name:   example_file_proc
'''

import sys

#һ���Զ�ȡ
def one_time_reading(filepath):
    with open(filepath, 'r') as f:
        print f.read()
        
#�̶��ֽڶ�ȡ
def fixed_bytes_reading(filepath, num):
    f = open(filepath, 'r')
    content=""
    try:
        while True:
            chunk = f.read(8)
            if not chunk:
                break
            content+=chunk
    finally:
        f.close()
        print content

#���ж�ȡ
def readinline(filepath): 
    f = open(filepath, "r")
    content=""
    try:
        while True:
            line = f.readline()
            if not line:
                break
            content+=line
    finally:
        f.close()
        print content

#һ���Զ�ȡ������
def readallline(filepath):
    filepath='D:/data.txt' 

    with open(filepath, "r") as f:
        txt_list = f.readlines()

    for i in txt_list:
        print i, 
#д�ļ�
def write(filepath,content):
    #w�Ḳ��ԭ�����ļ���a�����ļ�ĩβ׷��
    with open(filepath,"w") as f:
        f.write(content)
        
     