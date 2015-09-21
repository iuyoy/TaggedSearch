#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Global.config import *
from Tagged.get_data import *
from Tagged.web_tags import Web_tags
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

class Search_insite(object):
    def __init__(self):
        super(Search_insite,self).__init__()
    def run(self,web_id):
        result = Web_tags().run(id = web_id,return_tag = True)
        (words,level1_tags,level2_tags,title,content) = result
        level1_tags = sorted(level1_tags.items(), lambda x,y: cmp(x[1][2], y[1][2]), reverse=True)
        level2_tags = sorted(level2_tags.items(), lambda x,y: cmp(x[1][2], y[1][2]), reverse=True)
        return {'words':words,'level1_tags':level1_tags,'level2_tags':level2_tags,'title':title,'content':content}
if __name__ == '__main__':
    sftbw = Search_for_tags_by_word()
    print sftbw.run('公司')