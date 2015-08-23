#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')

from ini import *
from Scripts.db_op import Db_op as DB
from wikidata.wikidata_query import Wikidata_query as WikiQuery
#from wikidata.wikidata_parse import Wikidata_parse as WikiParse
from wikidata.wikidata_parse import Parse_stackly as Parse_Stackly

class generate_tags(object):
    parse_run = Parse_Stackly()
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(generate_tags,self).__init__()
        self.db.connect()
    #整合各部操作
    def run(self):
        entity_dicts = self.get_entity()
        for entity_dict in entity_dicts:
            for entity in entity_dict:
                self.get_dif_meanings_by_wikidata_query(u'苹果')
                return
    #数据库中读取
    def get_entity(self,limit = 10,offset = 0):
        sql = 'SELECT word_name FROM `%s` AS w,`%s` AS p  WHERE w.property = p.part_of_speech AND p.is_need = 1\
        LIMIT %d OFFSET %d' %(words_table,word_properties_table,int(limit),int(offset))
        row_num = self.db.select(sql)
        return self.db.fetchAllRows()

    #得到实体不同的意向
    def get_dif_meanings_by_wikidata_query(self,query_name):
        wikiquery = WikiQuery()
        wikiquery.run(query_name)
        #print wikiquery.parameters['totalhits']
        for i in wikiquery.result.itemlist:
            PS.append(i['title'])
            self.parse_run.run()
    #得到意向的可能的标签
    def get_tags_by_wikidata_parse(self):
        return
    #建立实体与意向的标签
    def build_ralations(self):
        return
    
if __name__ == '__main__':
    gt = generate_tags()
    #gt.run()
    parse_run = Parse_Stackly()
    parse_stack.append('q1')
    parse_run.run()
    print 'generate_tags',parse_stack
