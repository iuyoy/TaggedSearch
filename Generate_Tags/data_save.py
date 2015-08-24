#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

sys.path.append('..')
from Scripts.db_op import Db_op as DB
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
            sql = "SELECT is_ok FROM `%s` WHERE wikidata_id = '%s'" %(wikidata_entities_table,wikidata_id)
            result = self.db.select(sql)
            is_ok = 0
            if (result == True):
                is_ok = self.db.fetchOneRow()[0]
            #print sql,is_ok,result
            if (is_ok != 1):
                wikidata_type = self.db.SQL_filter(entity.pop('type'))
                sql_entity = "INSERT INTO `%s`(`wikidata_id`,`type`,`is_ok`) VALUES('%s','%s',%d)" %(wikidata_entities_table,wikidata_id,wikidata_type,2)
                print ("Start to insert %s entity into db ") %(wikidata_id)
                id = self.db.insert(sql_entity)
                ret = False
                if (id != 0):
                    sql_part_1 = "INSERT INTO `%s`(" %(wikidata_entity_properties_table)
                    sql_part_2 = "entity_id"
                    sql_part_3 = ") VALUES("
                    sql_part_4 = "%s" %(id)
                    sql_part_5 = ")"
                    for (property_name,values) in entity.items():
                       ret = self.save_entity_property1(sql_part_1,sql_part_2,sql_part_3,sql_part_4,sql_part_5,property_name,values)
                if(ret):
                    print ("Insert properties successfully")
                    sql_entity = "UPDATE `%s` SET is_ok = 1 WHERE id = %d" %(wikidata_entities_table,id)
                    ret = self.db.update(sql_entity)
                    if (ret):
                        print ("Insert %s entity into db successfully") %(wikidata_id)
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

    
class Wikidata_query_save_with_word_by_db(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Wikidata_query_save_with_word_by_db,self).__init__()
        self.db.connect()
    def save_result(self,word_name,word_id,wikidata_id):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "INSERT INTO %s (word_id,wikidata_id) VALUES(%d,'%s')" %(wikidata_word_table,int(word_id),wikidata_id)
        ret = self.db.insert(sql)
        return ret
    