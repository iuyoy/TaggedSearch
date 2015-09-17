#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

from config import *

def printout(str,level = 1):
    if(level >= print_level):
        try:
            print str
        except Exception,e:
            record_error(e)
            print str.encode('utf-8')

def record_error(error_info):
    try:
        open('error.txt','a').write(error_info+'\n')
    except:
        open('error.txt','a').write(str(error_info)+'\n')