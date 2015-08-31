#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import jieba
import jieba.posseg as pseg

class Word_segment(object):
    def __init__(self):
        return super(Word_segment, self).__init__()
    def run(self,str,flag = False,mode = False):
        return self.segment(str,flag = False,mode = False)

    def segment(self,str,flag = False,mode = False):
        if (flag):
            words = pseg.cut(str)
            return words
        else:
            seg_list = jieba.cut(str, cut_all=mode)
            return seg_list
if __name__ == "__main__":
    ws = Word_segment()
    ws.segment(" --word-item(-wi) [num]:执行num次wbsearchentities,否则1次")
    ws.segment(" --word-item(-wi) [num]:执行num次wbsearchentities,否则1次",True,False)
    ws.segment(" --word-item(-wi) [num]:执行num次wbsearchentities,否则1次",True,True)
