#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

sys.path.append('..')
from Scripts.db_op import Db_op as DB
from Scripts.code import print_whatever_code as printout
from ini import *
#直接写入文件来保存数据
class Data_save_by_file(object):
    def __init__(self):
        super(Data_save_by_file,self).__init__()
    def write(self,content,filename='tags_test.txt',mode = 'a'):
        fp = open(filename,mode)
        fp.write(content)

#直接写入数据库来保存数据
class Data_save_by_db(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Data_save_by_db,self).__init__()
        self.db.connect()
    def save_entity(self,entity):
        if(entity.has_key('id')):
            wikidata_id = self.db.SQL_filter(entity.pop('id'))
            wikidata_type = self.db.SQL_filter(entity.pop('type'))
            #保存wikidata_entity的项
            sql_entity = "INSERT INTO `%s`(`wikidata_id`,`type`,`is_ok`) VALUES('%s','%s',%d)" %(wikidata_entities_table,wikidata_id,wikidata_type,1)
            ret = self.db.insert(sql_entity)
            #保存entity对应的属性
            if (ret):
                sql_part_1 = "INSERT INTO `%s`(" %(wikidata_entity_properties_table)
                sql_part_2 = "entity_id"
                sql_part_3 = ") VALUES("
                sql_part_4 = "'%s'" %(wikidata_id)
                sql_part_5 = ")"
                for (property_name,values) in entity.items():
                    ret = self.save_entity_property1(sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,property_name,values)
            #如果存在的话，更改wikidata_id对应的wikidata_word中记录的is_ok为1
            if(ret):
                try:
                    sql_entity = "UPDATE `%s` SET is_ok = 1 WHERE wikidata_id = '%s'" %(wikidata_word_table,wikidata_id)
                    self.db.update(sql_entity)
                except Exception,e:
                    record_error(str(e))
            return ret
    #保存实体属性时 确保property_name的一对一对应的property_name部分
    def save_entity_property1(self,sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,property_name,values):
        sql_part_2 += ',property_name'
        sql_part_4 += ",'%s'" %(self.db.SQL_filter(property_name))
        values_type = type(values)
        ret = False
        if (values_type == list):
            ret = True
            for value in values:
                ret = self.save_entity_property2(sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,value)
        elif(values_type == str):
            ret = self.save_entity_property2(sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,values)  
        return ret   
    #保存实体属性时 确保property_name和value的一对一对应的value部分         
    def save_entity_property2(self,sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,value):
        sql_part_2 += ',value'
        sql_part_4 += ",'%s'" %(self.db.SQL_filter(value))
        sql = sql_part_1+sql_part_2+sql_part_3+sql_part_4+sql_part_5
        ret = self.db.insert(sql)
        if(ret > 0):
            return True
        else:
            return False
    def save_deleted_item(self,wikidata_id):
        try:
            wikidata_id = self.db.SQL_filter(wikidata_id)
            sql_entity = "UPDATE `%s` SET is_ok = 3 WHERE wikidata_id = '%s'" %(wikidata_word_table,wikidata_id)
            self.db.update(sql_entity)
        except Exception,e:
            record_error(str(e))
    
class Wikidata_query_save_with_word_by_db(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Wikidata_query_save_with_word_by_db,self).__init__()
        self.db.connect()
    def save_result(self,word_id,wikidata_id,is_ok = 0):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT EXISTS(SELECT * FROM %s WHERE word_id = %d AND wikidata_id = '%s')" %(wikidata_word_table,int(word_id),wikidata_id)
        ret = self.db.select(sql)
        if (ret):
            is_exist = self.db.fetchOneRow()[0]
            if (not is_exist):
                sql = "INSERT INTO %s (word_id,wikidata_id,is_ok) VALUES(%d,'%s',%d)" %(wikidata_word_table,int(word_id),wikidata_id,int(is_ok))
                ret = self.db.insert(sql)
            else:
                return True
        return ret
    