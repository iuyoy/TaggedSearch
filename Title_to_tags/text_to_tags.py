#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Word_Segment.word_segment import *
from get_data import *

#存放词语的数据结构
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

#文本->标签
class Text_to_tags(object):
    word_dict = Word_Dict()
    level1_tags = {}
    level2_tags = {}
    key_words = []
    need_pos =['n','vn','eng']
    def __init__(self):
        super(Text_to_tags,self).__init__()
    def run(self,id = 0,choose = 0):
        article = self.get_article(id)
        if (article != []):
            ret = self.get_words(article)
            self.get_keywords(article)
        if (choose):
            for word_name,(count,part_of_speech) in self.word_dict.wd.items():
               for np in self.need_pos:
                   if np in part_of_speech:
                       print word_name
                       self.get_tag(word_name.encode('utf-8'))
                       break
            temp_tags1 = sorted(self.level1_tags.items(), key=lambda d: d[1],reverse=True) 
            temp_tags2 = sorted(self.level2_tags.items(), key=lambda d: d[1],reverse=True) 
            for i,j in temp_tags1:
                try:
                    print i[0],j,Get_wikidata().get_name(i[0])[0]
                except:
                    print i[0],j
            print ('----------------------------------------------------')
            for i,j in temp_tags2:
                try:
                    print i[0],j,Get_wikidata().get_name(i[0])[0]
                except:
                    print i[0],j
        else:
            self.reset_tags()
            for word_name in self.key_words:
                print word_name
                self.get_tag(word_name.encode('utf-8'))
            temp_tags1 = sorted(self.level1_tags.items(), key=lambda d: d[1],reverse=True) 
            temp_tags2 = sorted(self.level2_tags.items(), key=lambda d: d[1],reverse=True) 
            for i,j in temp_tags1:
                try:
                    print i[0],j,Get_wikidata().get_name(i[0])[0]
                except:
                    print i[0],j
            print ('----------------------------------------------------')
            for i,j in temp_tags2:
                try:
                    print i[0],j,Get_wikidata().get_name(i[0])[0]
                except:
                    print i[0],j
               
    #得到文章
    def get_article(self,id = 0):
        article = Get_article().get_one_cnbeta_article(id)
        return article
    #article 结构[id,title,content]
    #得到词语
    def get_words(self,article,reset = False):
        if (article != []):
            (id,title,content) = article
            word_segment = Word_segment()
            title_words = word_segment.segment(title,False,True)
            all_words = word_segment.segment(content,False,True)
            if (reset):
                self.word_dict.reset()
            self.word_dict.put_words_in(title_words)
            self.word_dict.put_words_in(all_words)
            return True
        return False
    def get_keywords(self,article,reset = False):
        if (article != []):
            (id,title,content) = article
            word_segment = Word_segment()
            self.key_words = word_segment.get_keywords(title,False,True)
            self.key_words.extend(word_segment.get_keywords(content))
           
            return True
        return False
    #得到标签
    def get_tag(self,word): 
         gt = Get_tags()
         level1_tags = gt.get_all_level1_tags(word)
         level2_tags = gt.get_all_level2_tags(word)
         for tag in level1_tags:
             if (tag in self.level1_tags):
                 self.level1_tags[tag] += 1
             else:
                 self.level1_tags[tag] = 1
         for tag in level2_tags:
             if (tag in self.level2_tags):
                 self.level2_tags[tag] += 1
             else:
                 self.level2_tags[tag] = 1
    def reset_tags(self):
        self.level1_tags.clear()
        self.level2_tags.clear()

if __name__ == '__main__':
    ttt = Text_to_tags()
    ttt.run(53619)
    #print Get_wikidata().get_name('q89')[0]
    #ttt.get_tag('苹果')