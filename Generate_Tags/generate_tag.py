﻿#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from ini import *
from Scripts.db_op import Db_op as DB
from Scripts.code import print_whatever_code as printout
from wikidata.wbsearchentities import Wbsearchentities as Wikisearch
from wikidata.wikidata_parse import Wikidata_parse as WikiParse
from wikidata.wikidata_parse import Parse_stackly as Parse_Stackly
from wikidata.wikidata_parse import Wikidata_parse as WP
from data_save import Wikidata_query_save_with_word_by_db as Save_Query
from get_data import *

class generate_tag(object):
    parse_run = Parse_Stackly()
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(generate_tag,self).__init__()
        self.db.connect()
    #整合各部操作
    def get_save_words_item(self,times = 1):
        for i in range(times):
            word = self.get_word()
            if(word != False):
                self.query_and_save_word(word)
            else:
                printout ("Not any word.")
    #数据库中读取
    def get_word(self):
        return Get_word().run()
        
    #查找词语的不同意向，并将关系存入数据库    
    def query_and_save_word(self,word):
        (word_id,word_name) = word
        printout ("WikiSearch:%s is running" %(word_name))
        wikisearch = Wikisearch()
        item_list = wikisearch.run(word_name)
        save = Save_Query()
        printout ("Save:%s is running. Total records:%d" %(word_name,len(item_list)))
        if (item_list != []):
            for item in item_list:
                ret = save.save_result(word_id,item['id'])
                if(not ret):
                    printout ("Error:save word wikidata_item error")
            printout("Search and save %s successfully. Total records:%d" %(word_name),len(item_list))
        else:
            ret = save.save_result(word_id,'',2)
            printout("Search and save %s successfully, but there is not any search result." %(word_name))
        return True

    #得到意向的可能的标签
    def get_tags_by_wikidata_parse(self):
        return
    #建立实体与意向的标签
    def build_ralations(self):
        return
    
if __name__ == '__main__':
    gt = generate_tag()
    if(len(sys.argv)>1):
        gt.get_save_words_item(int(sys.argv[1]))
    else:
        gt.get_save_words_item(1)
    