#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created on 2009-9-4

    @author: lingjie
    @name : example_html_proc
'''
import urllib2, sys
from htmlentitydefs import entitydefs
from HTMLParser import HTMLParser

class exhtml(HTMLParser):
    def __init__(self):
        self.Hn = ["" for i in range(5)]
        self.readingHn = [False for i in range(5)]
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attr):
        sHn = ["h%d"%i for i in range(1,6)]
        if tag in sHn:
            self.readingHn[sHn.index(tag)] = True

    def handle_data(self, data):
        for i in range(5):
            if self.readingHn[i]:
               self.Hn[i] += data
        
    def handle_endtag(self, tag):
        sHn = ["h%d"%i for i in range(1,6)]
        if tag in sHn:
            self.readingHn[sHn.index(tag)] = False

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name])
        else:
            self.handle_data("&" + name + ":")

    def getHn(self,index):
        return self.Hn[index]

if __name__ == "__main__":
    url = "http://www.gnu.org/"
    try:
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "error: ", e
        sys.exit(1)

    tp = exhtml()
    tp.feed(fd.read())    
    for i in range(5):
        print "h%d : %s"%(i+1,tp.getHn(i))
    tp.close()