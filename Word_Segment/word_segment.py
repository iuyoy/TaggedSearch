#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import jieba
import jieba.posseg as pseg
import jieba.analyse

class Word_segment(object):
    def __init__(self):
        return super(Word_segment, self).__init__()

    #search=true是搜索模式；mode=false为精确模式，true为全模式；flag为带词性
    #mode,falg,search不能同时使用,优先级顺序为search>flag>mode
    def segment(self,string,mode = False,flag = False,search=False):
        if (search):
            words = jieba.cut_for_search(string)
        elif (flag):
            words = pseg.cut(string)
        else:
            words = jieba.cut(string, cut_all=mode)
        return words
    #提取关键词 mode=0为textrank，mode=1为TF-IDF
    def get_keywords(self,string,mode = 0,num = 20,withWeight = False,allowPOS = ('ns', 'n', 'vn', 'v')):
        if (mode):
            return jieba.analyse.extract_tags(string, topK=num, withWeight=withWeight, allowPOS=allowPOS)
        else:
            return jieba.analyse.textrank(string, topK=num, withWeight=withWeight, allowPOS=allowPOS)

if __name__ == "__main__":
    ws = Word_segment()
    str = '12345678901234567890'
    ws.segment(str)
    print u"全模式"
    for i in ws.segment(str,mode = True):
        print i
    print u"精确模式"
    for i in ws.segment(str,flag = True):
        print i
    print u"搜索模式"
    for i in  ws.segment(str,search = True):
        print i