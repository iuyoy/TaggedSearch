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
    filter_pos = ['x']
    def __init__(self,filter_pos = ''):
        super(Web_tags,self).__init__()
        if (filter_pos != ''):
            self.set_filter_pos(filter_pos)

    def run(self,id= 0,filter_pos = ''):
        self.clear_words()
        if (filter_pos != ''):
            self.set_filter_pos(filter_pos)
        ret = self.get_web(id)
        if (ret):
            self.get_words()
            self.add_word()

    def get_web(self,id = 0):
        web = Get_web().get_one_cnbeta_article(id)
        if (web):
            (self.web_id,self.title,self.content) = web
            return True
        else:
            return False
    def get_words(self):
        self.words.extend(pseg.lcut(self.title))
        self.words.extend(pseg.lcut(self.content))
        
    def add_word(self):
        for word_name,pos in self.words:
            printout(2,word_name,pos)
            word_name = word_name.encode('utf-8')
            if (pos not in self.filter_pos):
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
    def build_relation(self,word_id,word_name):
        #wbsearch查询得到relations
        relation_list = Wbsearch().run(word_name)
        result = True
        for relation in relation_list:
            result = Save_word().add_word_entity_relation(word_id,relation['id'])
        if(result):
            Save_word().change_word_sign(word_id,1)

    def set_filter_pos(self,filter_pos):
        self.filter_pos = filter_pos
    def add_filter_pos(self,filter_pos):
        self.filter_pos.extend(filter_pos)
    def clear_words(self):
        self.words = []
if __name__ == "__main__":
    wt = Web_tags()
    for i in range(51200,51250):
        print i
        wt.run(i)
        print 