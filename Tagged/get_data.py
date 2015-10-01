#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append('..')
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

class Get_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Get_data, self).__init__()
        self.connect()
    def connect(self):
        try:
            self.db.connect()
        except:
            pass
    def return_oneresult(self,result):
        if(result):
            return self.db.fetchOneRow()
        else:
            return False
    def __delete__(self):
        try:
            self.db.close()
        except:
            pass

class Get_website(Get_data):
    def __init__(self):
        super(Get_website, self).__init__()
    def get_one_cnbeta_article(self,id = 0):
        id = int(id)
        if (id == 0):
            sql = "SELECT id,title,content FROM `%s`.`%s` WHERE `level` = 0 AND id > 53000 LIMIT 1  " %(search_db,cnbeta_table)
        else:
            sql = "SELECT id,title,content FROM `%s`.`%s` WHERE `level` = 0 AND id = %d" %(search_db,cnbeta_table,id)
        result = self.db.select(sql)
        if(result):
            return self.db.fetchOneRow()
        else:
            return []
    def get_sogou_news_by_id(self,id=0,number=1,offset=0,sign=0):
        id = int(id)
        number = int(number)
        sign = int(sign)
        sql = "SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+\
            "` WHERE `sign` = %s AND id >= %s LIMIT %s OFFSET %s"
        para = (sign,id,number,offset)
        result = self.db.select(sql,para)
        if(result):
            return self.db.fetchAllRows()
        else:
            return []
class Get_entity(Get_data):
    def __init__(self):
        super(Get_entity, self).__init__()
    def get_id(self,wikidata_id):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT id,sign FROM `"+wiki_db+"`.`"+entities_table+"` WHERE wikidata_id = %s"
        para = [wikidata_id]
        result = self.db.select(sql,para)
        return self.return_oneresult(result)

    def get_entity_by_word(self,word_name = '',word_id = 0,):
        if (word_id == 0):
            word = Get_word().check_word(word_name)
            if(word):
                word_id = word[0]
        word_id = int(word_id)
        sql = "SELECT we.id,we.wikidata_id,\
        IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
        AS `name`\
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we , `"+wiki_db+"`.`"+word_entity_table+"` AS wwe \
        WHERE wwe.entity_id = we.id AND wwe.word_id = %s AND we.sign = 1"
        para = [word_id]
        entities = self.db.select(sql,para)
        if entities:
            return self.db.fetchAllRows()
        return False  
    def get_deep_entity_by_word(self,word_name = '',word_id = 0):
        if (word_id == 0):
            word = Get_word().check_word(word_name)
            if(word):
                word_id = word[0]
        word_id = int(word_id)
        sql = "SELECT we.id,wikidata_id,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
        AS `name`,`property_name`,count(we.id) AS `count`\
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we , `"+wiki_db+"`.`"+word_entity_table+"` AS wwe , `"+wiki_db+"`.`"+entity_properties_table+"` AS wep\
        WHERE wwe.entity_id = wep.entity_id AND we.wikidata_id = wep.property_value AND wwe.word_id = %s AND we.sign = 1\
        GROUP BY id ORDER BY `count` DESC"
        para = [word_id]
        entities = self.db.select(sql,para)
        if entities:
            return self.db.fetchAllRows()
        return False  
    def get_all_entity_name(self,language):
        language = self.db.SQL_filter(language)
        sql = "SELECT DISTINCT `"+language+"` FROM `"+wiki_db+"`.`"+entities_table+"` WHERE `"+language+"` != '' AND sign = 1"
        entities = self.db.select(sql)
        if entities:
            return self.db.fetchAllRows()
        return False  

class Get_word(Get_data):
    def __init__(self):
        super(Get_word, self).__init__()
    #得到word，也可用于判断word是否存在
    def check_word(self,word_name,pos = ''):
        word_name = self.db.SQL_filter(word_name)
        pos = self.db.SQL_filter(pos)
        sql = "SELECT `id`,`word_name`,`pos`,`sign` FROM `"+wiki_db+"`.`"+words_table+"` WHERE word_name = %s"
        para = [word_name]
        result = self.db.select(sql,para)
        if(result):
            return self.db.fetchOneRow()
        return result

class Get_alias(Get_data):
    def __init__(self):
        super(Get_alias, self).__init__()
    def get_all_aliases_value(self):
        sql = "SELECT DISTINCT `value` FROM `"+wiki_db+"`.`"+entity_aliases_table+"` WHERE sign = 0"
        entities = self.db.select(sql)
        if entities:
            return self.db.fetchAllRows()
        return False  