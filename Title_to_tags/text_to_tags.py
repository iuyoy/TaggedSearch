#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Word_Segment.word_segment import *
from get_data import *

class Text_to_tags(object):
    word_dict = Word_Dict()
    def __init__(self):
        super(Text_to_tags,self).__init__()
    def run(self):
        article = self.get_article()
        if (article != []):
            ret = self.get_words(article)
        if (ret):
            change_to_tag()
    #得到文章
    def get_article(self):
        article = Get_article().get_one_cnbeta_article()
        return article
    #article 结构[id,title,content]
    #得到词语
    def get_words(self,article,reset = False):
        if (article != []):
            (id,title,conetent) = article
            word_segment = Word_segment()
            title_words = word_segment.segment(title,False,True)
            all_words = word_segment.segment(content,False,True)
            if (reset):
                self.word_dict.reset()
            word_dict.put_words_in(title_words)
            word_dict.put_words_in(all_words)
            return True
        return False
     #得到标签
     def get_tag(self,word): 

class Word_Dict(object):
    wd = {}
    #wd = {'word':['count',['part_of_speech']]}
    def __init__(self,words = None):
        super(Word_Dict,self).__init__()
        if(words is not None):
            self.reset()
            self.put_words_in(words)
    def put_words_in(self,words):
        for word in words:
            self.add_word(word)
    def add_word(self,word):
        (name,part_of_speech) = word
        #已有项，加个数
        if (name in self.wd):
            self.wd[name][0] = self.wd[name][0]+1
            #加词性
            if (part_of_speech not in self.wd[name][1]):
                self.wd[name][1].append(part_of_speech)
        #未有项，加项
        else:
            self.wd[name]=[1,[part_of_speech]]
    def reset(self):
        self.wd.clear()
if __name__ == '__main__':
    ttt = Text_to_tags()
    ttt.run()
