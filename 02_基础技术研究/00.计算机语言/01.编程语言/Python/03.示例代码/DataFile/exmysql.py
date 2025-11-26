#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    Created on 2014-11-20
    Updated on 2025-11-26
    
    @author: lingjie
    @name:   example_mysql_proc
'''

import os
import sys
from contextlib import contextmanager

try:
    import pymysql
    MYSQL_LIBRARY = "pymysql"
except ImportError:
    try:
        import mysql.connector
        MYSQL_LIBRARY = "mysql.connector"
    except ImportError:
        print("请安装 pymysql 或 mysql.connector: pip install pymysql")
        sys.exit(1)

@contextmanager
def db_cursor(connection):
    """数据库游标上下文管理器"""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

class MySQLManager:
    def __init__(self, user, password, host, database, port=3306):
        """
        初始化MySQL连接管理器
        
        Args:
            user (str): 用户名
            password (str): 密码
            host (str): 主机地址
            database (str): 数据库名
            port (int): 端口号，默认3306
        """
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.conn = None
        self.connect()

    def connect(self):
        """建立数据库连接"""
        try:
            if MYSQL_LIBRARY == "pymysql":
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor
                )
            else:  # mysql.connector
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    charset="utf8mb4",
                    autocommit=False
                )
            print(f"成功连接到数据库: {self.database}")
        except Exception as e:
            print(f"连接数据库失败: {e}")
            raise

    def insert(self, table, data_dict):
        """
        安全插入数据，使用参数化查询防止SQL注入
        
        Args:
            table (str): 表名
            data_dict (dict): 数据字典，键为列名，值为数据
        """
        if not data_dict:
            print("数据字典不能为空")
            return False
            
        try:
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s'] * len(data_dict))
            values = list(data_dict.values())
            
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with db_cursor(self.conn) as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                print(f"成功插入 {cursor.rowcount} 条记录到表 {table}")
                return True
        except Exception as e:
            print(f"插入数据失败: {e}")
            self.conn.rollback()
            return False

    def show_all(self, table, limit=None):
        """
        显示表中所有数据
        
        Args:
            table (str): 表名
            limit (int): 限制返回的记录数
        """
        try:
            sql = f"SELECT * FROM {table}"
            if limit:
                sql += f" LIMIT {limit}"
                
            with db_cursor(self.conn) as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                
                if not results:
                    print(f"表 {table} 中没有数据")
                    return []
                
                # 显示表头
                if results:
                    headers = results[0].keys() if isinstance(results[0], dict) else range(len(results[0]))
                    print("\t".join(str(h) for h in headers))
                    print("-" * 50)
                
                # 显示数据
                for row in results:
                    if isinstance(row, dict):
                        print("\t".join(str(row.get(h, "")) for h in headers))
                    else:
                        print("\t".join(str(item) for item in row))
                        
                return results
        except Exception as e:
            print(f"查询数据失败: {e}")
            return []

    def find_by_name(self, table, name):
        """
        根据名称查找记录
        
        Args:
            table (str): 表名
            name (str): 查找的名称
        """
        try:
            sql = f"SELECT * FROM {table} WHERE name = %s"
            
            with db_cursor(self.conn) as cursor:
                cursor.execute(sql, (name,))
                results = cursor.fetchall()
                
                if not results:
                    print(f"未找到名为 '{name}' 的记录")
                    return []
                
                for row in results:
                    print(row)
                return results
        except Exception as e:
            print(f"查找数据失败: {e}")
            return []

    def update_by_name(self, table, name, update_data):
        """
        根据名称更新记录
        
        Args:
            table (str): 表名
            name (str): 要更新的记录名称
            update_data (dict): 要更新的数据字典
        """
        if not update_data:
            print("更新数据不能为空")
            return False
            
        try:
            set_clause = ', '.join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values()) + [name]
            
            sql = f"UPDATE {table} SET {set_clause} WHERE name = %s"
            
            with db_cursor(self.conn) as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                print(f"成功更新 {cursor.rowcount} 条记录")
                return True
        except Exception as e:
            print(f"更新数据失败: {e}")
            self.conn.rollback()
            return False

    def delete_by_name(self, table, name):
        """
        根据名称删除记录
        
        Args:
            table (str): 表名
            name (str): 要删除的记录名称
        """
        try:
            sql = f"DELETE FROM {table} WHERE name = %s"
            
            with db_cursor(self.conn) as cursor:
                cursor.execute(sql, (name,))
                self.conn.commit()
                print(f"成功删除 {cursor.rowcount} 条记录")
                return True
        except Exception as e:
            print(f"删除数据失败: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def main():
    """示例用法"""
    # 配置数据库连接信息
    config = {
        'user': 'your_username',
        'password': 'your_password', 
        'host': 'localhost',
        'database': 'your_database',
        'port': 3306
    }
    
    try:
        # 使用上下文管理器自动管理连接
        with MySQLManager(**config) as db:
            # 示例数据
            users = {"owlman": "1350000000", "alice": "13800000000"}
            table_name = "myphone"
            
            # 插入数据
            for name, phone in users.items():
                db.insert(table_name, {"name": name, "phone": phone})
            
            # 显示所有数据
            print("\n=== 所有记录 ===")
            db.show_all(table_name)
            
            # 查找特定记录
            print("\n=== 查找 owlman ===")
            db.find_by_name(table_name, "owlman")
            
            # 更新记录
            print("\n=== 更新 owlman 的电话 ===")
            db.update_by_name(table_name, "owlman", {"phone": "13900000000"})
            
            # 再次显示
            print("\n=== 更新后的记录 ===")
            db.show_all(table_name)
            
    except Exception as e:
        print(f"数据库操作出错: {e}")

if __name__ == "__main__":
    main()
