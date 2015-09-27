#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

import sys,os
sys.path.append(sys.path[0]+'\..')

from Global.config import *
from Global.global_function import *
from Tagged.get_data import Get_entity
from Tagged.get_data import Get_alias
class add_words():
    origin_words = set()
    new_words = set()
    languages = {0:'label_zh-hans',1:'label_zh-cn',2:'label_zh',3:'aliases',4:'label_en'}
    def __init__(self):
        self.origin_words = set()
        self.new_words = set()
        return
    def auto_run(self,start = 0,end = 4):
        ret = self.get_origin_words()
        if (ret):
            printout(5,'Successfully get origin words.')
            dict_name = 'dict_auto.txt'
            for lang in range(int(start),int(end)):
                ret = self.get_new_words(lang)
                if (ret):
                    printout(5,'Successfully get new %s words.' %(self.languages[lang]))
                else:
                    printout(5,'Fail to get new %s words.' %(self.languages[lang]))
            ret = self.generate_new_dict(dict_name)
            if (ret):
                printout(5,'Successfully write new word_dict.')
                ret = self.merge_dict(dict_name)
                if ret:
                    printout(5,'Successfully merge word_dict.')
                else:
                    printout(5,'Fail to merge word_dict.')
            else:
                printout(5,'Fail to write new word_dict.')
           
        else:
            printout(5,'Fail to get origin words.')
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
        if lang > 4:
            lang = 0
        if lang == 3:
            entities = Get_alias().get_all_aliases_value()
        else:
            language = self.languages[lang]
            entities = Get_entity().get_all_entity_name(language)

        if entities:
            for entity in entities:
                name = self.delete_blank_and_colon(entity[0])
                if (name != False and name != '' and name not in self.origin_words):
                    self.new_words.add(name)
            return True
        return False
    #生成新词典
    def generate_new_dict(self,dict_name = 'wikidata_word_dict'):
        with open(dict_name,'w') as new_dict:
            content = ''
            printout(3,"total:%d" %(len(self.new_words)))
            for index,word in enumerate(self.new_words):
                try:
                    content += word+' 1 wd\n'
                except:
                    printout(2,word)
                    content += word.encode('utf-8')+' 1 wd\n'
                if index%10000 == 0:
                    printout(3,"total:%d finished %d " %(len(self.new_words),index))
            try:
                new_dict.write(content)
                return True
            except:
                ret = new_dict.write(content.encode('utf-8'))
                return True
        return False
    #去除有空格的词，去掉有分号的词分号前的部分
    def delete_blank_and_colon(self,word):
        if ' ' in word:
            return False
        if ':' in word:
            start = word.find(':')
            if word[start+1:0] != None:
                return word[start+1:]
        else:
            return word
    #合并新旧词典
    def merge_dict(self,new = 'wikidata_word_dict',ori = jieba_words_dict_path):
        # 备份旧字典
        with open(ori,'r') as ori_dict:
            with open(ori+'_bak','w') as bak_dict:
                bak_dict.write(ori_dict.read())
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
    aw.auto_run()
    #aw.run(3)
    aw.merge_dict('dict_auto.txt')