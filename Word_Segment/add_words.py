#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

import sys,os
sys.path.append(sys.path[0]+'\..')

from Global.config import *
from Global.global_function import *
from Tagged.get_data import Get_entity
class add_words():
    origin_words = set()
    new_words = set()
    languages = {0:'label_zh-hans',1:'label_zh-cn',2:'label_zh',3:'label_en'}
    def __init__(self):
        return 
    def run(self,lang = 0,dict_name = 'wikidata_word_dict'):
        ret = self.get_origin_words()
        if (ret):
            printout(5,'Successfully get origin words.')
            ret = self.get_new_words(lang)
            if (ret):
                printout(5,'Successfully get new words.')
                ret = self.generate_new_dict(dict_name)
                if (ret):
                    printout(5,'Successfully write new word_dict.')
                else:
                    printout(5,'Fail to write new word_dict.')
            else:
                printout(5,'Fail to get new words.')
        else:
            printout(5,'Fail to get origin words.')
    #得到旧词典中的词
    def get_origin_words(self):
        with open(jieba_words_dict_path,'r') as dict_file:
            for word in dict_file:
                word = unicode(word,'utf-8')
                self.origin_words.add(word.split()[0])
            return True
        return False
    #得到新单词
    def get_new_words(self,lang = 0):
        if lang >= 4:
            lang = 0
        language = self.languages[lang]
        entities = Get_entity().get_all_entity_name(language)
        if entities:
            for entity in entities:
                name = self.delete_blank_and_colon(entity[0])
                if (name != False and name not in self.origin_words):
                    self.new_words.add(name)
            return True
        return False
    #生成新词典
    def generate_new_dict(self,dict_name = 'wikidata_word_dict'):
        with open(dict_name,'w') as new_dict:
            content = ''
            for word in self.new_words:
                try:
                    content += word+' 1 wd\n'
                except:
                    printout(2,word)
                    content += word.encode('utf-8')+' 1 wd\n'
            try:
                printout(3,"total:%d" %(len(self.new_words)))
                new_dict.write(content)
                return True
            except:
                ret = new_dict.write(content.encode('utf-8'))
                return ret
        return False
    #去除有空格的词，去掉有分号的词分号前的部分
    def delete_blank_and_colon(self,word):
        if ' ' in word:
            return False
        if ':' in word:
            start = word.find(':')
            if word[start+1:0] != None:
                return word[start+1:]
        return False
    #合并新旧词典
    def merge_dict(self,new = 'wikidata_word_dict',ori = jieba_words_dict_path):
        with open(ori,'r') as ori_dict:
            with open(ori+'_bak','w') as bak_dict:
                bak_dict.write(ori_dict.read())
            ori_dict
        with open(ori,'a') as ori_dict:
            with open(new,'r') as new_dict:
                ori_dict.write(new_dict.read())
                return True
        return False
#需要处理的情况，去除一些分类的名字
#如（分类:目录）
#去除有空格的word

if __name__ == '__main__':
    aw = add_words()
    for i in range(3):
        dict_name = 'dict_'+str(i)+'.txt'
        aw.run(i,dict_name)
        aw.merge_dict(dict_name)