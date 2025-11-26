#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Created on 2009-9-11
    Updated on 2025-11-26

    @author: lingjie
    @name  : example_xml_proc
'''

import os
import sys
from xml.dom import minidom
from xml.etree import ElementTree as ET

class BookListManager:
    def __init__(self, xml_file_path):
        """
        初始化书籍列表管理器
        
        Args:
            xml_file_path (str): XML文件路径
        """
        self.xml_file_path = xml_file_path
        self.document = None
        self.root = None
        self.load_xml()

    def load_xml(self):
        """加载XML文件"""
        try:
            if not os.path.exists(self.xml_file_path):
                self.create_empty_xml()
                return
                
            self.document = minidom.parse(self.xml_file_path)
            self.root = self.document.documentElement
            print(f"成功加载XML文件: {self.xml_file_path}")
        except Exception as e:
            print(f"加载XML文件失败: {e}")
            self.create_empty_xml()

    def create_empty_xml(self):
        """创建空的XML文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.xml_file_path), exist_ok=True)
            
            # 创建根元素
            root = ET.Element("booklist")
            tree = ET.ElementTree(root)
            
            # 美化XML并保存
            self._prettify_xml(tree, self.xml_file_path)
            
            # 重新加载
            self.document = minidom.parse(self.xml_file_path)
            self.root = self.document.documentElement
            print(f"创建新的XML文件: {self.xml_file_path}")
        except Exception as e:
            print(f"创建XML文件失败: {e}")

    def _prettify_xml(self, tree, file_path):
        """美化XML格式并保存"""
        rough_string = ET.tostring(tree.getroot(), encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        
        with open(file_path, 'wb') as f:
            f.write(pretty_xml)

    def print_list(self):
        """打印所有书籍信息"""
        if not self.root:
            print("XML文档未加载")
            return
            
        try:
            print("\n=== 书籍列表 ===")
            books = self.root.getElementsByTagName("book")
            
            if not books:
                print("没有找到书籍记录")
                return
                
            for book in books:
                title = ""
                comment = ""
                
                title_elements = book.getElementsByTagName("title")
                if title_elements and title_elements[0].childNodes:
                    title = title_elements[0].childNodes[0].nodeValue
                    
                comment_elements = book.getElementsByTagName("comment")
                if comment_elements and comment_elements[0].childNodes:
                    comment = comment_elements[0].childNodes[0].nodeValue
                
                print(f"书名: {title}")
                print(f"  评价: {comment}\n")
                
        except Exception as e:
            print(f"打印书籍列表失败: {e}")

    def add_book(self, title, comment):
        """
        添加新书籍
        
        Args:
            title (str): 书名
            comment (str): 评价
        """
        if not self.document or not self.root:
            print("XML文档未加载")
            return False
            
        try:
            # 检查是否已存在相同书名的书籍
            if self.find_book(title):
                print(f"书名为 '{title}' 的书籍已存在")
                return False
            
            # 创建book元素
            book_element = self.document.createElement("book")
            self.root.appendChild(book_element)

            # 创建title元素
            title_element = self.document.createElement("title")
            title_text = self.document.createTextNode(title)
            title_element.appendChild(title_text)
            book_element.appendChild(title_element)

            # 创建comment元素
            comment_element = self.document.createElement("comment")
            comment_text = self.document.createTextNode(comment)
            comment_element.appendChild(comment_text)
            book_element.appendChild(comment_element)

            # 保存到文件
            self.save_xml()
            print(f"成功添加书籍: {title}")
            return True
            
        except Exception as e:
            print(f"添加书籍失败: {e}")
            return False

    def find_book(self, title):
        """
        查找指定书名的书籍
        
        Args:
            title (str): 书名
            
        Returns:
            list: 匹配的书籍元素列表
        """
        if not self.root:
            return []
            
        try:
            books = self.root.getElementsByTagName("book")
            matching_books = []
            
            for book in books:
                title_elements = book.getElementsByTagName("title")
                if title_elements and title_elements[0].childNodes:
                    book_title = title_elements[0].childNodes[0].nodeValue
                    if book_title == title:
                        matching_books.append(book)
                        
            return matching_books
        except Exception as e:
            print(f"查找书籍失败: {e}")
            return []

    def update_book(self, title, new_title=None, new_comment=None):
        """
        更新书籍信息
        
        Args:
            title (str): 原书名
            new_title (str): 新书名
            new_comment (str): 新评价
        """
        if not new_title and not new_comment:
            print("没有提供更新内容")
            return False
            
        books = self.find_book(title)
        if not books:
            print(f"未找到书名为 '{title}' 的书籍")
            return False
            
        try:
            for book in books:
                if new_title:
                    title_elements = book.getElementsByTagName("title")
                    if title_elements and title_elements[0].childNodes:
                        title_elements[0].childNodes[0].nodeValue = new_title
                        
                if new_comment:
                    comment_elements = book.getElementsByTagName("comment")
                    if comment_elements and comment_elements[0].childNodes:
                        comment_elements[0].childNodes[0].nodeValue = new_comment
                        
            self.save_xml()
            print(f"成功更新书籍: {title}")
            return True
        except Exception as e:
            print(f"更新书籍失败: {e}")
            return False

    def delete_book(self, title):
        """
        删除指定书名的书籍
        
        Args:
            title (str): 书名
        """
        books = self.find_book(title)
        if not books:
            print(f"未找到书名为 '{title}' 的书籍")
            return False
            
        try:
            for book in books:
                self.root.removeChild(book)
                
            self.save_xml()
            print(f"成功删除书籍: {title}")
            return True
        except Exception as e:
            print(f"删除书籍失败: {e}")
            return False

    def save_xml(self):
        """保存XML到文件"""
        if not self.document:
            print("XML文档未加载")
            return False
            
        try:
            # 美化XML格式
            pretty_xml = self.document.toprettyxml(indent="  ", encoding='utf-8')
            
            with open(self.xml_file_path, 'wb') as f:
                f.write(pretty_xml)
            return True
        except Exception as e:
            print(f"保存XML文件失败: {e}")
            return False

def main():
    """示例用法"""
    # 创建XML文件路径
    xml_file = "data/booklist.xml"
    
    # 创建管理器实例
    book_manager = BookListManager(xml_file)
    
    # 添加书籍
    book_manager.add_book("Python编程", "一本很好的Python入门书籍")
    book_manager.add_book("算法导论", "经典的算法教材")
    book_manager.add_book("数据库系统概念", "深入浅出的数据库教程")
    
    # 显示所有书籍
    book_manager.print_list()
    
    # 查找书籍
    print("=== 查找书籍 ===")
    found_books = book_manager.find_book("Python编程")
    if found_books:
        print(f"找到书籍: {len(found_books)} 本")
    
    # 更新书籍
    print("\n=== 更新书籍 ===")
    book_manager.update_book("Python编程", new_comment="更新后的评价：非常棒的Python教程")
    
    # 再次显示
    book_manager.print_list()
    
    # 删除书籍
    print("=== 删除书籍 ===")
    book_manager.delete_book("算法导论")
    
    # 最终显示
    print("\n=== 最终书籍列表 ===")
    book_manager.print_list()

if __name__ == "__main__":
    main()
