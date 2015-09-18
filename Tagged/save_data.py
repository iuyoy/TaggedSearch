#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append('..')
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

class Save_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Save_data, self).__init__()
        self.connect()
    def connect(self):
        try:
            self.db.connect()
        except:
            pass
    def __delete__(self):
        try:
            self.db.close()
        except:
            pass

class Words(Save_data):
    def __init__(self):
        super(Words, self).__init__()
    #得到word，也可用于判断word是否存在
    def check_word(self,word_name,pos):
        word_name = self.db.SQL_filter(word_name)
        pos = self.db.SQL_filter(pos)
        sql = "SELECT `id`,`word_name`,`sign` FROM `"+wiki_db+"`.`"+words_table+"` WHERE word_name = %s"
        para = [word_name]
        result = self.db.select(sql,para)
        if(result):
            return self.db.fetchOneRow()
        return result
    #添加新word
    def add_word(self,word_name,pos,sign = 0):
        word_name = self.db.SQL_filter(word_name)
        pos = self.db.SQL_filter(pos)
        sign = int(sign)
        sql = "INSERT INTO `"+wiki_db+"`.`"+words_table+"` (`word_name`, `pos`, `sign`) VALUES (%s, %s, %s)"
        para = [word_name,pos,sign]
        id = self.db.insert(sql,para)
        return id
    #修改word sign
    def change_word_sign(self,word_id,sign = 0):
        word_id = int(word_id)
        sign = int(sign)
        sql = "UPDATE `"+wiki_db+"`.`"+words_table+"` SET `sign` = %s WHERE `id` = %s"
        para = [sign,word_id]
        result = self.db.update(sql,para)
        return result
    #添加word和entity的关系
    def add_word_entity_relations(self,word_id,word_name,sign = 0):
        word_id = int(word_id)
        word_name = self.db.SQL_filter(word_name)
        sign = int (sign)
        sql = "INSERT INTO `"+wiki_db+"`.`"+word_entity_table+"` \
        (`word_id`,`entity_id`,`sign`) \
        SELECT "+str(word_id)+",id,"+str(sign)+" FROM entities \
        WHERE `label_zh-hans` LIKE '%"+word_name+"%'\
        OR `label_zh-cn` LIKE '%"+word_name+"%'\
        OR `label_zh` LIKE '%"+word_name+"%'\
        OR `label_en` LIKE '%"+word_name+"%'\
        OR `description_zh-hans` LIKE '%"+word_name+"%'\
        OR `description_zh-cn` LIKE '%"+word_name+"%'\
        OR `description_zh` LIKE '%"+word_name+"%'\
        OR `description_en` LIKE '%"+word_name+"%'\
        "
        result = self.db.insert(sql)
        return result
    #查询出