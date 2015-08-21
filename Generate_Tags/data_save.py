#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

#直接写入文件来保存数据
class Data_save_by_file(object):
    def __init__(self):
        super(Data_save_by_file,self).__init__()
    def write(self,content,filename='tags_test.txt',mode = 'a'):
        fp = open(filename,mode)
        fp.write(content)

#直接写入数据库来保存数据
class Data_save_by_db(object):
    def __init__(self):
        super(Data_save_by_db,self).__init__()
    