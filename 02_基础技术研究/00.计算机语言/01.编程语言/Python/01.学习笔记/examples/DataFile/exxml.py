#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created on 2009-9-11

    @author: lingjie
    @name  : example_xml_proc
'''

from xml.dom import minidom, Node
import sys

class booklist:
    def __init__(self, doc):
        self.document = minidom.parse(doc)
        self.root = self.document.documentElement

    def printlist(self):
        title = comment = ""
        for book in self.root.childNodes:
            if(book.nodeType != Node.ELEMENT_NODE):
                continue
            if (book.tagName == "book"):
                for item in book.childNodes:
                    if item.nodeType != Node.ELEMENT_NODE:
                        continue
                    if item.tagName == "title":
                        title = item.childNodes[0].wholeText
                    if item.tagName == "comment":
                        comment = item.childNodes[0].wholeText
            print "%s\n\t%s" % (title, comment)

    def addbook(self, title, comment):
        book = self.document.createElement("book")
        self.root.appendChild(book)

        titlenode = self.document.createElement("title")
        titlenode.appendChild(self.document.createTextNode(title))
        book.appendChild(titlenode)

        commentnodde = self.document.createElement("comment")
        commentnodde.appendChild(self.document.createTextNode(comment))
        book.appendChild(commentnodde)


    def delbook(self, title):
        pass

if __name__ == "__main__":
    domdoc = booklist("data/booklist.xml")
    domdoc.addbook("the database", "This is a greast book,and i like it.")
    domdoc.printlist()
