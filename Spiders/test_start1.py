# -*- coding: utf-8 -*-
import time
import re
class test():
    a = 1
    prefix = 'http://m.cnbeta.com/wap/view_'
    postfix = '.htm'
    def __init__(self):
        print self.a
        self.joint_url(a)
        print self.a
    def plus(self):
        self.a+=1
    def joint_url(self,id):
        print self.prefix+str(id)+self.postfix
        return self.prefix+str(id)+self.postfix

def time_test():
    string = '时间:2015-08-02 10:55:24'
    pattern = re.compile(':([0-9:\- ]+)')
    rs = pattern.search(string)
    if rs != None:
        string = rs.groups()[0]
    print string
    string = time.mktime(time.strptime(string,'%Y-%m-%d %H:%M:%S'))
    print string
    print type(string)

def sql():
    string = "%s%s%s" %(1,2,3)
    #string = "%s%s%s" %(1,2)
    #string += "" %(3)
    print string

if __name__ == "__main__":
    #b = test()
    time_test()
    #sql()