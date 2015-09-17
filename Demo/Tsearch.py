#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
from config import *
from search.get_data import *

class search_for_tags_by_words(object):
    def __init__(self):
        super(search_for_tags_by_words,self).__init__()
    def run(self):
        return
    
class Search_for_tags_by_word(object):
    def __init__(self):
        super(Search_for_tags_by_word,self).__init__()
    def run(self,word):
        gwe = get_wikidata_entity()
        level1_tags = gwe.get_meaningnames_by_wordname(word)
        level2_tags = gwe.get_tagnames_by_wordname(word)
        return (level1_tags,level2_tags)

if __name__ == '__main__':
    sftbw = Search_for_tags_by_word()
    print sftbw.run('公司')