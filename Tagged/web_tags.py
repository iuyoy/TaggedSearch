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
class Web_tags(object):
    web_id = 0
    title = ''
    content = ''
    words = []
    def __init__(self):
        super(Web_tags,self).__init__()
    def run(self,id= 0):
        ret = self.get_web(id)
        if (ret):
            self.get_words()
    def get_web(self,id = 0):
        web = Get_web().get_one_cnbeta_article(id)
        if (web):
            (self.web_id,self.title,self.content) = web
            return True
        else:
            return False
    def get_words(self):
        word = pseg.lcut(self.title)
        print self.title
        new_word = Words()
        for word_name,pos in word:
            print word_name,pos
            word_name = word_name.encode('utf-8')
            if (pos not in ['x']):
                result = new_word.check_word(word_name,pos)
                sign = -1
                if (result != False):
                    (word_id,word_name,sign) = result
                    word_name = word_name.encode('utf-8')
                else:
                    word_id = new_word.add_word(word_name,pos)
                    if(word_id):
                        sign = 0
                if (sign == 0):
                    result = new_word.add_word_entity_relations(word_id,word_name)
                    if(result):
                        new_word.change_word_sign(word_id,1)
if __name__ == "__main__":
    wt = Web_tags()
    for i in range(50000,51000):
        wt.run(i)