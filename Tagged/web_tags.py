#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append(sys.path[0]+'/..')

from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import *
from lru import LRUCache
from jieba import posseg as pseg
import jieba

from Wikidata.api_wbsearchentities import Wbsearchentities as Wbsearch

class Website_entities(object):
    #过滤的词性'x','p','ul','f','d','c','l','uj','a','r','s','an','ad','u','m','k','y'
    filter_pos = []
    #停止词
    stop_words = set()
    
    number_per_select = 1
    #已经遍历的website数
    offset = 0
    default_pos = 'wt'
    #id:count
    words = {}
    #type:0,1,2,3,5,6
    #(id,type):count
    tags={}
    db = DB(dbinfo = dbinfo)
    def __init__(self,filter_pos = [],stop_words = '',cache_items = 1000):
        super(Website_entities,self).__init__()
        self.set_filter_pos(filter_pos)
        self.set_stop_words(stop_words)
        #用于存已经查询过的word
        #word_name:(word_id,set())
        self.word_cache = LRUCache(cache_items)
        self.db.connect()
    #自动执行的入口
    def auto_run(self,start_id = 0,number = 0):
        if(start_id <= 0):
            start_id = self.get_new_sogou_website_id()
            if(start_id and start_id[0] ):
                start_id = int(start_id[0])+1
            else:
                start_id = 1
        while(True):
            if(number<=0):
                websites = self.get_website(start_id,self.number_per_select)
                start_id += self.number_per_select
            else:
                websites = self.get_website(start_id,number)
            if websites:
                for website in websites:
                    self.clear_mem()
                    (website_id,url,docno,title,content,sign) = website
                    printout(3,'Start website_id:%d' %(website_id))
                    (titile_words,content_words) = self.segment_words(title,content)
                    self.website_tags(website_id,titile_words,True)
                    self.website_tags(website_id,content_words,True)
                    printout(2,'    Start build_relations:%d' %(website_id))
                    self.build_all_relations(website_id)
            if(number>0 or not websites):
                return True
    #得到最大的没有检索过的website_id
    def get_new_sogou_website_id(self):  
        sql = "SELECT max(`website_id`) FROM `"+wiki_db+"`.`"+websites_words_table+"`"
        result = self.db.select(sql)
        return self.db.fetchOneRow()          
    #建立索引(website-words&tags)
    def website_tags(self,website_id,words,have_pos = True):
        if have_pos:
            for word_name,pos in words:
                word_name = word_name.encode('utf-8')
                if (pos not in self.filter_pos and word_name not in self.stop_words):
                    ret = self.get_word_tags(website_id,word_name,pos)
        else:
            for word_name in words:
                word_name = word_name.encode('utf-8')
                if (word_name not in self.stop_words):
                    ret =  self.get_word_tags(website_id,word_name,self.default_pos)
    #建立所有连接
    def build_all_relations(self,website_id,rank=0):
        for word_id,count in self.words.items():
            sql = "INSERT INTO `"+wiki_db+"`.`"+websites_words_table+"`(`website_id`,`word_id`,`count`,`sign`,`rank`) VALUES(%s,%s,%s,%s,%s)" 
            para = (website_id,word_id,count,0,rank)
            ret = self.db.insert(sql,para)
        for (entity_id,sign),count in self.tags.items():
            sql = "INSERT INTO `"+wiki_db+"`.`"+websites_tags_table+"`(`website_id`,`entity_id`,`count`,`sign`,`rank`) VALUES(%s,%s,%s,%s,%s)" 
            para = (website_id,entity_id,count,sign,rank)
            ret = self.db.insert(sql,para)
    #得到website对应的words和tags
    def get_word_tags(self,website_id,word_name,pos):
        #如果word在cache中，从中提取word_id,和tag_ids
        if word_name in self.word_cache.key_order:
            (word_id,tags) = self.word_cache[word_name]
            self.add_words(word_id,1)
            for (tag_id,tag_type,count) in tags:
                self.add_tags(tag_id,tag_type,count)
        else:#如果不在
            #(id,word_name,pos,sign)
            word = self.get_word(word_name,pos)
            if word:
                (word_id,name,pos,sign) = word
                self.add_words(word_id,1)
                if sign == 1:
                    tags = self.get_tags(word_id)
                else:
                    tags = []
                self.word_cache[word_name] =(word_id,tags)#加入cache
                for (tag_id,tag_type,count) in tags:
                    self.add_tags(tag_id,tag_type,count)
    #words的增加或新建
    def add_words(self,id,count=1):
        if id in self.words:
            self.words[id]+=count
        else:
            self.words[id] = count
    #tags的增加或新建
    def add_tags(self,tag_id,tag_type,count):
        if (tag_id,tag_type) in self.tags:
            self.tags[(tag_id,tag_type)] += count
        else:
            self.tags[(tag_id,tag_type)] = count

    #查询得到word 
    def get_word(self,word_name,pos):
        word_name = self.db.SQL_filter(word_name)
        pos = self.db.SQL_filter(pos)
        sql = "SELECT `id`,`word_name`,`pos`,`sign` FROM `"+wiki_db+"`.`"+words_table+"` WHERE word_name = %s"
        para = [word_name]
        result = self.db.select(sql,para)
        if(result):
            word = self.db.fetchOneRow()
        else:
            word = result
        if (not word):
            sign = 0
            word_id = self.add_word(word_name,pos,sign = sign)
            self.build_word_tag_relation(word_id,word_name)
            word = (word_id,word_name,pos,sign)
        return word
    def add_word(self,word_name,pos,sign):
        word_name = self.db.SQL_filter(word_name)
        pos = self.db.SQL_filter(pos)
        sign = int(sign)
        sql = "INSERT INTO `"+wiki_db+"`.`"+words_table+"` (`word_name`, `pos`, `sign`) VALUES (%s, %s, %s)"
        para = [word_name,pos,sign]
        id = self.db.insert(sql,para)
        return id
    #建立word和tag的关系
    def build_word_tag_relation(self,word_id,word_name):
        #wbsearch查询得到relations
        relation_list = Wbsearch().run(word_name)
        result = True
        for relation in relation_list:
            result = self.add_word_entity_relation(word_id,relation['id'])
        if(result):
            self.change_word_sign(word_id,1)
    def change_word_sign(self,word_id,sign = 0):
        word_id = int(word_id)
        sign = int(sign)
        sql = "UPDATE `"+wiki_db+"`.`"+words_table+"` SET `sign` = %s WHERE `id` = %s"
        para = [sign,word_id]
        result = self.db.update(sql,para)
        return result
    def add_word_entity_relation(self,word_id,wikidata_id,sign = 0):
        word_id = int(word_id)
        entity = self.get_entity_id(wikidata_id)
        sign = int(sign)
        if (entity):
            (entity_id,sign) = entity
            sign = int(sign)
            sql = "INSERT INTO `"+wiki_db+"`.`"+word_entity_table+"`(`word_id`,`entity_id`,`sign`) VALUES(%s,%s,%s)" 
            para = [word_id,entity_id,sign]
            ret = self.db.insert(sql,para)
        else:
            return -1
        return ret
    def get_entity_id(self,wikidata_id):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT id,sign FROM `"+wiki_db+"`.`"+entities_table+"` WHERE wikidata_id = %s"
        para = [wikidata_id]
        result = self.db.select(sql,para)
        return self.db.fetchOneRow()
    #得到标签
    def get_tags(self,word_id):
        tags = []
        l1_tags = self.get_l1_tags(word_id)
        if(l1_tags):
            for id in l1_tags:
                tags.append([id[0],0,1])
            l2_tags = self.get_l2_tags(word_id)
            if(l2_tags):
                for id,property_type,count in l2_tags:
                    tags.append([id,property_type,count])
            return tags
        else:
            printout(0,"Not any tags!")
            return []
    def get_l1_tags(self,word_id = 0,):
        word_id = int(word_id)
        sql = "SELECT we.id \
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we , `"+wiki_db+"`.`"+word_entity_table+"` AS wwe \
        WHERE wwe.entity_id = we.id AND wwe.word_id = %s AND we.sign = 1"
        para = [word_id]
        entities = self.db.select(sql,para)
        if entities:
            return self.db.fetchAllRows()
        return False  
    def get_l2_tags(self,word_id = 0):
        word_id = int(word_id)
        sql = "SELECT we.id,`property_name`,count(we.id) AS `count`\
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we , `"+wiki_db+"`.`"+word_entity_table+"` AS wwe , `"+wiki_db+"`.`"+entity_properties_table+"` AS wep\
        WHERE wwe.entity_id = wep.entity_id AND we.wikidata_id = wep.property_value AND wwe.word_id = %s AND we.sign = 1\
        GROUP BY id ORDER BY `count` DESC"
        para = [word_id]
        entities = self.db.select(sql,para)
        if entities:
            return self.db.fetchAllRows()
        return False  
    #得到一个web页面内容
    def get_website(self,id=0,number=1,sign=0):
        id = int(id)
        number = int(number)
        sign = int(sign)
        sql = "SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+\
            "` WHERE `sign` = %s AND id >= %s LIMIT %s"
        para = (sign,id,number)
        result = self.db.select(sql,para)
        if(result):
            return self.db.fetchAllRows()
        else:
            return False
    #分词
    def segment_words(self,title,content):
        title_words = pseg.lcut(title)
        content_words = pseg.lcut(content)
        return (title_words,content_words)
    #设置过滤的词性
    def set_filter_pos(self,filter_pos):
        if type(filter_pos) == dict:
            self.filter_pos = filter_pos
    def add_filter_pos(self,filter_pos):
        pos_type = type(filter_pos)
        if pos_type == dict:
            self.filter_pos.extend(filter_pos)
            return True
        elif pos_type == str:
            self.filter_pos.append(filter_pos)     
            return True
        return False       
    #设置停止词set
    def set_stop_words(self,stop_words = ''):
        words_type = type(stop_words)
        #str则当作路径
        if (words_type == str and stop_words != ''):
            try:
                with open(stop_words,'r') as stopwords:
                    self.stop_words |= set(stopwords.read().split())
                    return True
            except Exception,e:
                printout(5,e)
                while 1:
                    go_on = raw_input("Y:continue , N:stop | Your choice:")
                    if go_on[0] == 'y' or go_on[0] == 'Y':
                        break;
                    if go_on[0] == 'n' or go_on[0] == 'N':
                        sys.exit()
                return False
        elif(words_type == set):
            self.stop_words |= stop_words
            return True
        elif(words_type == list):
            self.stop_words |= set(stop_words)
            return True
        else:
            return False 
    #设置自动建立标签时，一次select获得的website数
    def set_nps(self,nps):
        self.number_per_select = int(nps)
    #设置缺省pos
    def set_default_pos(self,pos):
        if (type(pos) == str):
            self.default_pos = pos
    #清空words,l1_tags,l2_tags
    def clear_mem(self):
        self.words = {}
        self.tags = {}

if __name__ == "__main__":
    we = Website_entities(stop_words = stopwords_path,cache_items=2000)
    we.auto_run(1,0)
            