#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

from config import *
#按等级输出
def printout(level = 1,*strings):
    if(level >= print_level):
        for string in strings:
            try:
                print string,
            except Exception,e:
                error_info = str(e) + " | print string error"
                record_error(error_info)
                try:
                    print string.encode('utf-8'),
                except Exception,e:
                    error_info = str(e) + " | print utf_8 encode string error"
                    record_error(error_info)
                    try:
                        print string.encode('raw_unicode_escape'),
                    except Exception,e:
                        error_info = str(e) + " | print raw_unicode_escape string error"
                        record_error(error_info)
        print 
#记录错误信息
def record_error(error_info):
    try:
        open('error.txt','a').write(error_info+'\n')
    except:
        open('error.txt','a').write(str(error_info)+'\n')

#python unicode中间码
def modify_charater(string):
    try:
        return unicode(string,'utf8')
    except:
        try:
            return string.decode('utf8')
        except:
            return string