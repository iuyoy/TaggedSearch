#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
from gensim import corpora, models, similarities

class websites_sort(object):
    corpus=[]
    vec=[]
    def __init__(self):
        super(websites_sort, self).__init__()
    def set_vec(self,words,l1_tag,l2_tags):
        count = 0
        for word_id in words:
            self.vec.append([count,1]) 
    def clear(self):
        self.corpus = []
        self.vec = []
