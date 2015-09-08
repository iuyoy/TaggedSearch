#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')

from ini import *
from Scripts.db_op import Db_op as DB
from Scripts.code import print_whatever_code as printout
from wikidata.wbsearchentities import Wbsearchentities as Wikisearch
from wikidata.wikidata_parse import Parse_Orderly as Wiki_parse
from data_save import Wikidata_query_save_with_word_by_db as Save_Query
from get_data import *

class Word_entity(object):
    def __init__(self):
        super(Word_entity,self).__init__()
    #根据词语查询意向，并将关系存入数据库
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
            printout("Search and save %s successfully. Total records:%d" %(word_name,len(item_list)))
        else:
            ret = save.save_result(word_id,'',2)
            printout("Search and save %s successfully, but there is not any search result." %(word_name))
        return True

#获取wikidata_entity的可以作为标签的属性
class Get_entity_tag(object):
    def __init__(self):
        super(Get_entity_tag,self).__init__()
    #times=0则一直运行直到结束
    def run(self,times = 1):
        is_over = False
        if(times <= 0):
            times = -1
            printout(u'预计还有 条需要检索',3)
        else:
            printout(u'预计还有%d条需要检索' %(times),3)
        while((not is_over) and (times != 0)):
            wikidata_id = self.get_wiki_entity()
            if (times > 0):
                    times -= 1
            if (wikidata_id != []):
                parse_queue.put(wikidata_id)
                printout("Main Wikidata_parse:%s is running." %(wikidata_id)) 
                ret = self.get_tags_by_wikidata_parse()
                if(ret):
                    printout("Main Wikidata_parse and save:%s successfully." %(wikidata_id))
            else:
                is_over = True
                printout("Not any wikidata_entity.")
                return True
        if (times == 0):
            return True
        return False
    def get_wiki_entity(self):
        return Get_wikidata_entity().run(1)
    #得到意向的可能的标签
    def get_tags_by_wikidata_parse(self):
        wp = Wiki_parse()
        return wp.run()
class build_tag_library(object):
    def __init__(self):
        super(build_tag_library,self).__init__()
    def run(self,times = 1):
        word = self.get_word()
        self.judge(word)
    #建立实体与意向的标签
    def build_ralations(self):
        return
    def get_word(self):
        gwft = Get_word_for_tag()
        word_mean = gwft.run()
        self.get_meaning_tags(word_mean)
    def judge(self,word_mean):
        return
    def get_meaning_tags(self,meaning):
        return
if __name__ == '__main__':
    usage =u"""Generate_Tag usage:
        --word-item(-wi) [num]:执行num次wbsearchentities,否则1次
        --entity-tags(-et) [num]:执行num次get_entity_tags,否则1次
        --build-tags(-bt) [num]:执行num次build_tag_library,否则1次
        """
    if(len(sys.argv)>1):
        if(sys.argv[1] == '--word-item' or sys.argv[1] == '-wi'):
            gt = Word_entity()
            try:
                int(sys.argv[2])
            except:
                sys.argv[2] = 1
            gt.get_save_words_item(int(sys.argv[2]))
        elif(sys.argv[1] == '--entity-tag' or sys.argv[1] == '-et'):
            et = Get_entity_tag()
            try:
                int(sys.argv[2])
            except:
                sys.argv[2] = 1
            et.run(int(sys.argv[2]))
        elif(sys.argv[1] == '--build-tags' or sys.argv[1] == '-bt'):
            bt = build_tag_library()
            try:
                int(sys.argv[2])
            except:
                sys.argv[2] = 1
            bt.run(int(sys.argv[2]))
        else:
            printout(usage,9)
    else:
        printout(usage,9)
    