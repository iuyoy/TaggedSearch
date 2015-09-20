#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from config import *
from Tagged.get_data import *
class search(object):
    def __init__(self):
        super(search,self).__init__()
    def run(self):
        return
class search_tags_by_words(object):
    def __init__(self):
        super(search_tags_by_words,self).__init__()
    def run(self):
        return
    
class Search_tags_by_word(object):
    def __init__(self):
        super(Search_tags_by_word,self).__init__()
    def run(self,word):
        ge = Get_entity()
        level1_tags = ge.get_entity_by_word(word)
        if(not level1_tags):
            level1_tags = []
        level2_tags = ge.get_deep_entity_by_word(word)
        if(not level2_tags):
            level2_tags = []
        return (level1_tags,level2_tags)

if __name__ == '__main__':
    sftbw = Search_for_tags_by_word()
    print sftbw.run('公司')