#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from ini import *
from Scripts.db_op import Db_op as DB
from Scripts.code import print_whatever_code as printout
#爬取数据时获取word_name和word_id的类
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
#构建标签库时的类
class Get_word_for_tag(Get_word):
    def __init__(self):
        super(Get_word_for_tag,self).__init__()
    #具体操作，最终结果为(word_id,word_name,[(wikidata_id,label,[aliases，····])，···])
    def get_from_db(self):
        word = self.get_word()
        if(word != False):
            (word_id,word_name,meaning_id) = word
            print word_id,word_name,meaning_id
            meaning = self.get_meaning(meaning_id)
            #if(meanings != False):
            return (word_id,word_name,meaning)
        return False
    #得到word_id和word_name
    def get_word(self):
        sql = "SELECT w.word_name,w.id,ww.wikidata_id FROM `%s` AS ww,`%s` AS w WHERE ww.word_id = w.id AND ww.is_ok = 1 LIMIT %d" %(wikidata_word_table,words_table,1)
        result = self.db.select(sql)
        if(result):
            result = self.db.fetchOneRow()
            word_name = result[0]
            word_id = result[1]
            meaning_id = result[2]
            return (word_id,word_name,meaning_id)
        return False
    #得到意向的 名字和别名 以及 可能的标签
    def get_meaning(self,meaning_id):
        #meaning = (word_id,word_name,(meaning_id,label,[aliases,·····],[tag_label·····]))     
        #得到名字  
        label_list = self.get_meaning_property(meaning_id,'labels',1)
        if(label_list != False):
            label = label_list[0]
            #得到别名
            aliases = []
            aliases_lists = self.get_meaning_property(meaning_id,'aliases',0)
            if(aliases_lists != False):
                for aliase_list in aliases_lists:
                    aliases.append(aliase_list[0])
            #得到标签
            tags = self.get_meaning_tags(meaning_id)
            if (tags != []):
                meaning = (meaning_id,label,aliases,tags)
                return meaning
        return False

    #得到实体的各种属性
    def get_meaning_property(self,wikidata_id,property_name = 'labels',one = 1):
        property_name = self.db.SQL_filter(property_name)
        sql = "SELECT wep.`value` FROM `%s` AS wep , `%s` AS we WHERE we.wikidata_id = wep.entity_id AND we.wikidata_id = '%s' AND wep.property_name = '%s'" %(wikidata_entity_properties_table,wikidata_entities_table,wikidata_id,property_name)
        result = self.db.select(sql)
        if(result):
            if(one == 1):
                meanings = self.db.fetchOneRow()
            else:
                meanings = self.db.fetchAllRows()
            return meanings
        return False
    #得到实体可以成为Tag的属性的值
    def get_meaning_tags(self,meaning_id):
        tags=[]
        for tag_property_name in ['father_classification','main_classification','property','belong_to']:
            tag_ids = self.get_meaning_property(meaning_id,tag_property_name,one = 0)
            print tag_ids
            if(tag_ids != False):
                for tag_id in tag_ids:
                    tag_name = self.get_meaning_property(tag_id[0],'labels',one = 1)
                    if (tag_name != False):
                        tags.append(tag_name)
        return tags
#获取wikidata_entity的类
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
 
class Get_tags(Get_word):
    def __init__(self):
        super(Get_tags,self).__init__()
    def get_from_db(self,wikidata_id):
        sql = ""
if __name__ == '__main__':
    ge = Get_word_for_tag()
    word = ge.run()
    print word

        
    
