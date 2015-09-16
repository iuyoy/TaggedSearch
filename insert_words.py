#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

sys.path.append('..')
from Scripts.db_op import Db_op as DB

class Insert_words(object):
    table = 'words'
    db = None
    def __init__(self,host = 'localhost',user = 'root',passwd = 'root',db = 'test',table = 'words',port = 3306,charset = 'utf8'):
        self.db = DB(host,user,passwd,db,port,charset)
        self.db.connect()
        self.set_table(table)
    def insert(self,word_name,word_property,word_from):
        word_name = self.db.SQL_filter(word_name)
        word_property = self.db.SQL_filter(word_property)
        word_from = self.db.SQL_filter(word_from)
        sql = "INSERT INTO %s(`word_name`,`property`,`from`) VALUES(\'%s\',\'%s\',\'%s\')" %(self.table,word_name,word_property,word_from)
        return self.db.insert(sql)

    def insert_from_txt(self,file_name):
        fp = open(file_name)
        count = 0
        for line in fp:
            word = line.split('	')
            count += 1
            id = self.insert(word[0],word[1],u'nlpcn.org') 
            if (count % 100 == 0):
                print id
    
    
    def set_table(self,table):
        self.table = self.db.SQL_filter(table)
    

def insert_word_properties(file_name):
    fp = open(file_name)
    db = DB('23.244.180.241','search','search&Tagged','search')
    db.connect()
    for line in fp:
        word = line.split(' ')
        sql = "INSERT INTO word_properties(`part_of_speech`,`property_name`,`comment`) VALUES(\'%s\',\'%s\',\'%s\')" %(word[0],word[1],'HanLP词性标注集') 
        print db.insert(sql)
        
        
def insert_words():
    iw = Insert_words('23.244.180.241','search','search&Tagged','search')
    if (len(sys.argv)>1):
        iw.insert_from_txt(sys.argv[1])
    else:
        iw.insert_from_txt(u'worddict360.txt')
       
if __name__ == '__main__':
    if (len(sys.argv)>1):
        insert_word_properties(argv[1])
    else:
        insert_word_properties('word_properties2.txt')
       
