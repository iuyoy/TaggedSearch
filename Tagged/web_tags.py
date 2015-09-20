#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append(sys.path[0]+'\..')
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

import jieba
import jieba.posseg as pseg
from get_data import Get_web
from Word_Segment.word_segment import Word_segment

from save_data import *
from get_data import *
from Wikidata.api_wbsearchentities import Wbsearchentities as Wbsearch
class Web_tags(object):
    web_id = 0
    title = ''
    content = ''
    words = []
    used_words = []
    return_tag = False
    #tag:{'id':[wikidata_id,name,count]}
    level1_tags = {}
    level2_tags = {}
    #过滤的词性
    filter_pos = ['x','p','ul','f','d','c','l','uj','a','r','s','an','ad']
    def __init__(self,filter_pos = ''):
        super(Web_tags,self).__init__()
        if (filter_pos != ''):
            self.set_filter_pos(filter_pos)
    #运行的入口
    def run(self,id= 0,filter_pos = '',return_tag = False):
        self.set_return_tag(return_tag)
        self.clear_words()
        if (filter_pos != ''):
            self.set_filter_pos(filter_pos)
        ret = self.get_web(id)
        if (ret):
            self.get_words()
            self.add_word()
        if (return_tag):
            return (self.used_words,self.level1_tags,self.level2_tags)
        else:
            return self.used_words
    #得到一个web页面内容
    def get_web(self,id = 0):
        web = Get_web().get_one_cnbeta_article(id)
        if (web):
            (self.web_id,self.title,self.content) = web
            return True
        else:
            return False
    #得到页面里的词语
    def get_words(self):
        self.words.extend(pseg.lcut(self.title))
        self.words.extend(pseg.lcut(self.content))

    #将得到的词语添加到数据库中
    def add_word(self):
        for word_name,pos in self.words:
            #printout(2,word_name,pos)
            word_name = word_name.encode('utf-8')
            if (pos not in self.filter_pos):
                self.used_words.append([word_name,pos])
                word = Get_word().check_word(word_name,pos)
                sign = -1
                if (word != False):
                    (word_id,word_name,sign) = word
                    word_name = word_name.encode('utf-8')
                else:
                    word_id = Save_word().add_word(word_name,pos)
                    if(word_id):
                        sign = 0
                if (sign == 0):
                    self.build_relation(word_id,word_name)
                if (self.return_tag):
                        self.get_all_tags(word_name)

    #根据词语产生标签，建立联系存入数据库
    def build_relation(self,word_id,word_name):
        #wbsearch查询得到relations
        relation_list = Wbsearch().run(word_name)
        result = True
        for relation in relation_list:
            result = Save_word().add_word_entity_relation(word_id,relation['id'])
        if(result):
            Save_word().change_word_sign(word_id,1)
    #获取标签
    def get_all_tags(self,word):
        self.get_l1_tags(word)
        self.get_l2_tags(word)
    def get_l1_tags(self,word):
        l1_tags = Get_entity().get_entity_by_word(word)
        if(l1_tags):
            self.add_into_tags(l1_tags,1)
    def get_l2_tags(self,word):
        l2_tags = Get_entity().get_deep_entity_by_word(word)
        if(l2_tags):
            self.add_into_tags(l2_tags,2)
    #添加到tag列表
    def add_into_tags(self,tags,level = 1):
        if level == 1:
            tags_lib = self.level1_tags
            for tag in tags:
                if (tag[0] in tags_lib):
                    tags_lib[tag[0]][2] += 1
                else:
                    tags_lib[tag[0]]=[tag[1],tag[2],1]
        else:
            tags_lib = self.level2_tags
            for tag in tags:
                if (tag[0] in tags_lib):
                    tags_lib[tag[0]][2] +=1# tag[3]
                else:
                    tags_lib[tag[0]]=[tag[1],tag[2],1]#tag[3]]
        
    def set_filter_pos(self,filter_pos):
        self.filter_pos = filter_pos
    def add_filter_pos(self,filter_pos):
        self.filter_pos.extend(filter_pos)
    def clear_words(self):
        self.words = []
    def set_return_tag(self,return_tag):
        self.return_tag = return_tag

if __name__ == "__main__":
    wt = Web_tags()
    #51250
    for i in range(51200,51201):
        print i
        rs = wt.run(i,return_tag = True)
        (words,l1_tags,l2_tags) = rs
        #print wt.used_words
        for (a,b) in words:
            print a,b
        #sorted(l1_tags.items(), lambda x,y: cmp(x[1][2], y[1][2]), reverse=True) 
        #print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #for i in l1_tags:
        #    printout(2,i,l1_tags[i][0],l1_tags[i][1],l1_tags[i][2])


        tags = sorted(l2_tags.items(), lambda x,y: cmp(x[1][2], y[1][2]), reverse=True) 
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for id,entity in tags:
            (wiki_id,name,count) = entity
            printout(2,id,wiki_id,name,count)
            