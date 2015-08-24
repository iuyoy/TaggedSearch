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
from wikidata.wikidata_parse import Wikidata_parse as WP
from data_save import Wikidata_query_save_with_word_by_db as Save_Query
class generate_tags(object):
    parse_run = Parse_Stackly()
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(generate_tags,self).__init__()
        self.db.connect()
    #整合各部操作
    def run(self):
        word_dicts = self.get_word(1)
        for word_dict in word_dicts:
            self.get_dif_meanings_by_wikidata_query(word_dict)
            return
    #数据库中读取
    def get_word(self,limit = 10,offset = 0):
        sql = 'SELECT word_name,w.id FROM `%s` AS w,`%s` AS p  WHERE w.property = p.part_of_speech AND p.is_need = 1\
        LIMIT %d OFFSET %d' %(words_table,word_properties_table,int(limit),int(offset))
        row_num = self.db.select(sql)
        return self.db.fetchAllRows()

    #得到实体不同的意向
    def get_dif_meanings_by_wikidata_query(self,word): 
        word_name = word[0]
        word_id = word[1]
        print word_name.encode('utf-8'),word_id
        wikiquery = WikiQuery()
        ret = False
        while(not wikiquery.is_complete()):
            wikiquery.run(word_name)
            #print wikiquery.parameters['totalhits']
            for i in wikiquery.result.itemlist:
                parse_stack.append(i['title'])
                self.parse_run.run()
                ret = Save_Query().save_result(word_name,word_id,i['title'])
                if(ret != True):
                    print "Save_Query word:%s wikidata_id:%s error." %(word_name,i['title'])
        if(ret == True):
            print "Save_Query word:%s successfully." %(word_name)
    #得到意向的可能的标签
    def get_tags_by_wikidata_parse(self):
        return
    #建立实体与意向的标签
    def build_ralations(self):
        return
    
if __name__ == '__main__':
    gt = generate_tags()
    gt.run()
    