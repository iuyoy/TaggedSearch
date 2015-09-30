#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(sys.path[0]+'/..')
import time
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

class Import_sogou(object):
    path = ''
    start_line = 0
    db = DB(dbinfo = dbinfo)
    def __init__(self,path = 'news_tensite_xml.dat',start_line = 0):
        if (os.path.exists(path)):
            self.path = path
            self.start_line = start_line
            self.db.connect()
        else:
            printout(5,"No such file. Please check the path and try again.")
            self.path = ''
            self.start_line = -1
    def run(self,times = 0):
        with open(self.path,'r') as fp:
            self.find_root(fp)
            if times:
                for i in xrange(times):
                    self.read_one_record(fp)
            else:
                ret = True
                while(fp and ret):
                    ret = self.read_one_record(fp)
        """
     	数据格式：
        <doc>
        <url>页面URL</url>
        <docno>页面ID</docno>
        <contenttitle>页面标题</contenttitle>
        <content>页面内容</content>
        </doc>
        注意：content字段去除了HTML标签，保存的是新闻正文文本 
    """
    #读取一条记录
    def read_one_record(self,fp):
        if fp:
            content = ''
            while ( '<doc>' not in content ):
                content = fp.readline()
                if not content :
                    return False
            url = fp.readline()[5:-7]
            docno = fp.readline()[7:-9]
            title = fp.readline()[14:-16]
            content = fp.readline()[9:-11]
            fp.readline()
            if (content):
                id = self.save_one_record((url,docno,title.decode('gbk','ignore'),content.decode('gbk','ignore')),0)
                if (id and id%10000 == 0):
                    printout(2,"%d records has been saved!" %(id))
            return True
    def save_one_record(self,record,sign):
       
        sql = "INSERT INTO `"+search_db+"`.`"+sogou_sogou_table+"` (`url`, `docno`,`title`,`content`,`sign`) VALUES (%s, %s, %s ,%s ,"+str(sign)+")"
        id = self.db.insert(sql,record)
        return id     

    #找到开始的行
    def find_root(self,fp):
        for i in xrange(self.start_line):
            fp.readline()
if __name__ == '__main__':
    file_path = u'D:/ROW/DChuan2015/数据/搜狐/news_sohusite_xml.full/news_sohusite_xml.dat'
    IS = Import_sogou(file_path,0)
    IS.run(0)
 