#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append('..')
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

from get_data import *

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

class Save_word(Save_data):
    def __init__(self):
        super(Save_word, self).__init__()
   
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
    #返回-1没有wikidata_id对应的entity_id
    #返回False插入失败,True成功
    def add_word_entity_relation(self,word_id,wikidata_id,sign = 0):
        word_id = int(word_id)
        entity = Get_entity().get_id(wikidata_id)
        if (entity):
            (entity_id,sign) = entity
            sign = int(sign)
            sql = "INSERT INTO `"+wiki_db+"`.`"+word_entity_table+"`(`word_id`,`entity_id`,`sign`) VALUES(%s,%s,%s)" 
            para = [word_id,entity_id,sign]
            ret = self.db.insert(sql,para)
        else:
            return -1
        return ret

class Save_website(Save_data):
    def __init__(self):
        super(Save_website, self).__init__()
    def build_website_word_relation(self,website_id,word_id,count,sign,rank):
        sql = "INSERT INTO `"+wiki_db+"`.`"+websites_words_table+"`(`website_id`,`word_id`,`count`,`sign`,`rank`) VALUES(%s,%s,%s,%s,%s)" 
        para = (website_id,word_id,count,sign,rank)
        ret = self.db.insert(sql,para)
        return ret
    def build_website_tag_relation(self,website_id,entity_id,count,sign,rank):
        sql = "INSERT INTO `"+wiki_db+"`.`"+websites_tags_table+"`(`website_id`,`entity_id`,`count`,`sign`,`rank`) VALUES(%s,%s,%s,%s,%s)" 
        para = (website_id,entity_id,count,sign,rank)
        ret = self.db.insert(sql,para)
        return ret
   