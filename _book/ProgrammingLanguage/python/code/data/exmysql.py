#! /usr/bin/env python
'''
    Created on 2014-11-20
    
    @author: lingjie
    @name:   example_mysql_proc
'''
import MySQLdb
import os
import sys

class exmysql:
    def __init__(self, usr, pwd, host, db):
#        print "init......"
        self.user = usr
        self.passwd = pwd
        self.host = host
        self.database = db
        self.conn = MySQLdb.connect(host=self.host,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.database,
                                    charset="utf8")

    def insert(self, table, rcs={}):
        """the rcs must is a map...."""
        cur = self.conn.cursor()
        insertSql = "insert into %s values('%s','%s')"
        for key in rcs:
            cur.execute(insertSql % (table, key, rcs[key]))
        cur.close()
        self.conn.commit()

    def showall(self, table):
        cur = self.conn.cursor()
        cur.execute("select * from %s" % table)
        for data in cur.fetchall():
            print "%-10s %-10s" % data[0:2]
        cur.close()

    def findbyname(self, table, name):
        cur = self.conn.cursor()
        cur.execute("select * from %s where name='%s'" % (table, name))
        for data in cur.fetchall():
            print "%-10s %-10s" % data[0:2]
        cur.close()

    def updatebyname(self, table, name, phone):
        cur = self.conn.cursor()
        updateSql = "update %s set phone='%s' where name='%s'"
        cur.execute(updateSql % (table, phone, name))
        cur.close()
        self.conn.commit()

    def delete(self, table, name):
        cur = self.conn.cursor()
        delcmd = "delete from %s where name='%s'"
        cur.execute(delcmd % (table, name))
        cur.close()
        self.conn.commit()

    def __del__(self):
#        print "del........"
        self.conn.close()

if __name__ == "__main__":
    try:
        usrs = {"owlman":"1350000000"}
        tab = "myphone"
        obj = exmysql(usr="sq_owlman", pwd="00000000",
                      host="61.129.57.211", db="sq_owlman")
#        obj.insert(tab, usrs)
        obj.showall(tab)
    except Exception, e:
       print "Error:", e
       #pass
    finally :
        del obj
