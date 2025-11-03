#! /bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil

if __name__ == '__main__':
	print("当前目录：" + os.getcwd())
	print("脚本所在目录：" + sys.path[0])
	print("列出脚本所在目录下的文件：")
	print(os.listdir(sys.path[0]))
	
	print("切换至脚本所在目录。。。")
	os.chdir(sys.path[0])
	print("当前目录：" + os.getcwd())	
	
	print("创建example目录。。。")
	if(not os.path.exists("example")):
		os.mkdir("example")
	else:
		print("目录已经存在。。。")
	
	print("当前目录下的文件。。。")
	print(os.listdir(os.getcwd()))

	print("创建example目录的子目录。。。")
	if(not os.path.exists(r"example/sub")):
		os.makedirs(r"example/sub")
	else:
		print("sub子目录已经存在。。。")

	print("在example目录下创建hello.py脚本。。。")
	if(not os.path.exists(r"example/hello.py")):
		file = open(r"example/hello.py",'w')
		file.writelines(r"print('hello,world...')")
		file.close()
	else:
		print("hello.py已经存在。。。")
		file = open(r"example/hello.py",'r')
		print(file.readlines())
		file.close()

	os.system(r"python example/hello.py")

	shutil.copytree("example", "temp")
	os.system(r"python temp/hello.py")
	print("当前目录下的文件。。。")
	print(os.listdir(os.getcwd()))

	shutil.rmtree("temp")
	print("当前目录下的文件。。。")
	print(os.listdir(os.getcwd()))
