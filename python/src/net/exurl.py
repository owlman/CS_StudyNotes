#! /bin/env python
'''
    Created on 2009-8-26

    @author: lingjie
    @name : example_url_proc
'''
import urllib2
import urllib
import sys

class exurl:
    '''
    test urllib2
    '''
    def __init__(self, url, data=None):
        if data != None:
            url = url + "?" + urllib.urlencode([("value", data)])
        self.req = urllib2.Request(url)
        self.fobj = urllib2.urlopen(self.req)

    def headerinfo(self):
        info = self.fobj.info()
        for key, value in info.items():
            print  "%s = %s" % (key, value)

    def submitbypost(self, data):
        data = urllib.urlencode([("value", data)])
        self.fobj = urllib2.urlopen(self.req, data)

    def printdoc(self):
        while 1:
            data = self.fobj.read(1024)
            if not len(data):
                break
            sys.stdout.write(data)

    def __del__(self):
        self.fobj.close()
        del self.req
        #pass

if __name__ == "__main__":
    url = "http://www.gnu.org/"
    try:
        obj = exurl(url)
#        obj.submitbypost("lingjie")
        obj.headerinfo()
#        obj.printdoc()
    except Exception, e:
        print "error:" , e
 