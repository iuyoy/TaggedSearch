#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from ini import *
from Scripts.db_op import Db_op as DB

class Get_word(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Get_word,self).__init__()
        self.db.connect()
    
    def run(self):
       return self.get_from_db()
    #从数据库中获取下一个要query的词语，成功返回(id,name)，失败返回False
    def get_from_db(self):
        sql = "SELECT MAX(word_id) FROM %s" %(wikidata_word_table)
        result = self.db.select(sql)
        if(result):
            word_id = self.db.fetchOneRow()[0]
            if(word_id == None):
                word_id = 0
            word_id += 1
            return self.get_word_name_by_id(word_id)   
        return False
    #根据id得到word_name
    def get_word_name_by_id(self,word_id):
        sql = "SELECT word_name,w.id FROM `%s` AS w,`%s` AS p  WHERE w.property = p.part_of_speech AND p.is_need = 1 AND w.id >= %d\
        LIMIT %d" %(words_table,word_properties_table,word_id,1)
        result = self.db.select(sql)
        if(result):
            result = self.db.fetchOneRow()
            word_name = result[0]
            word_id = result[1]
            return (word_id,word_name)
        return False

class Get_wikidata_entity(Get_word):
    def __init__(self):
        super(Get_wikidata_entity,self).__init__()
    def run(self,limit = 1):
        return self.get_from_db(limit)
    def get_from_db(self,limit = 1):
        sql = "SELECT wikidata_id FROM %s WHERE is_ok = %d LIMIT %d" %(wikidata_word_table,0,int(limit))
        result = self.db.select(sql)
        if(result):
            if(limit == 1):
                wikidata_id = self.db.fetchOneRow()[0]
                return wikidata_id
            else:
                wikidata_id_lists = self.db.fetchAllRows()
                return wikidata_id_lists
        return []
    
if __name__ == '__main__':
    ge = Get_wikidata_entity()
    ge.run()
