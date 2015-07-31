#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#from:lingyue.wkl   
#desc: use to deal with ini
#---------------------
#2015-07-30 created
#---------------------
import sys,os
import ConfigParser

class INI(object):
    path = ''
    cp = None
    def __init__(self, path):
        super(INI,self).__init__()
        self.path = path
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(self.path)
    def read(self, section, key):
        result = ""
        try:
            result = self.cp.get(section, key)
        except:
            pass
        return result
    def readint(self, section, key):
        result = 0
        try:
            result = self.cp.getint(section, key)
        except:
            pass
        return result
    def write(self, section, key, value):
        try:
            if(not self.cp.has_section(section)):
                self.cp.add_section(section)
            self.cp.set(section, key, value)
            self.cp.write(open(self.path,'w'))
        except:
            return False
        return True

if __name__ == '__main__':
    ini = INI("a.ini")
    print ini.write('section','key','value')
    print ini.write('section','num','1')
    print ini.read('section','key')
    print ini.readint('section','num')