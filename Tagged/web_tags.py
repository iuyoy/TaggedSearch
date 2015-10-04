#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append(sys.path[0]+'/..')

from Global.config import *
from Global.global_function import *
from lru import LRUCache
from jieba import posseg as pseg
import jieba

from Tagged.get_data import Get_website
from Tagged.get_data import Get_word
from Tagged.get_data import Get_entity
from Tagged.save_data import Save_word
from Tagged.save_data import Save_website
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
    def __init__(self,filter_pos = [],stop_words = '',cache_items = 1000):
        super(Website_entities,self).__init__()
        self.set_filter_pos(filter_pos)
        self.set_stop_words(stop_words)
        #用于存已经查询过的word
        #word_name:(word_id,set())
        self.word_cache = LRUCache(cache_items)
    #自动执行的入口
    def auto_run(self,start_id = 0,number = 0):
        if(start_id <= 0):
            start_id = Get_website().get_new_sogou_website_id()
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
                    self.build_all_relations(website_id)
            if(number>0 or not websites):
                return True
                
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
    def build_all_relations(self,website_id):
        for word_id,count in self.words.items():
            Save_website().build_website_word_relation(website_id,word_id,count,0,0) 
        for (entity_id,sign),count in self.tags.items():
            Save_website().build_website_tag_relation(website_id,entity_id,count,sign,0) 
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
                tags = self.get_tags(word_id)
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
        word = Get_word().check_word(word_name)
        if (not word):
            sign = 0
            word_id = Save_word().add_word(word_name,pos,sign = sign)
            self.build_word_tag_relation(word_id,word_name)
            word = (word_id,word_name,pos,sign)
        return word
    #建立word和tag的关系
    def build_word_tag_relation(self,word_id,word_name):
        #wbsearch查询得到relations
        relation_list = Wbsearch().run(word_name)
        result = True
        for relation in relation_list:
            result = Save_word().add_word_entity_relation(word_id,relation['id'])
        if(result):
            Save_word().change_word_sign(word_id,1)
    #得到标签
    def get_tags(self,word_id):
        tags = []
        l1_tags = Get_entity().get_entity_by_word(word_id=word_id)
        if(l1_tags):
            for id,wiki_id,name in l1_tags:
                tags.append([id,0,1])
            l2_tags = Get_entity().get_deep_entity_by_word(word_id=word_id)
            if(l2_tags):
                for id,wiki_id,name,property_type,count in l2_tags:
                    tags.append([id,property_type,count])
            return tags
        else:
            printout(0,"Not any tags!")
            return []
    #得到一个web页面内容
    def get_website(self,id=0,number=1,offset=0):
        web = Get_website().get_sogou_news_by_id(id,number)
        if (web):
            return web
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
                printout(0,e)
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
    we.auto_run(0,0)
            