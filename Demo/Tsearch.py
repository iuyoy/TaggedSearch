#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
from ini import *
from search.get_data import *

class search_for_tags_by_words(object):
    def __init__(self):
        super(search_for_tags,self).__init__()
    def run(self):
        return
    
class Search_for_tags_by_word(object):
    def __init__(self):
        super(Search_for_tags_by_word,self).__init__()
    def run(self,word):
        result = get_wikidata_entity().get_tagnames_by_wordname(word)
        return result

    #def run(self,word):
    #    word_ids = self.get_wordid(word)
    #    meaning_ids = self.get_meaning_ids_from_wordids(word_ids)
    #    self.get_tag_ids(self,meaning_ids)
    #    #self.get_tags(word_ids)
    
    ##通过wikidata的id得到各个意向的标签
    ##level代表标签等级，1:father_classification,2:main_calssification,4:property,8:belong_to,二进制相加表示多选
    #def get_tag_ids(self,meaning_ids,level = 15):
    #    for meaning_id in meaning_ids:
    #        self.get_wikidata_property(meaning_id)
    #        return 
    #def get_wikidata_property(self,meaning_id,level = 15):
    #    tag_ids = []
    #    get_wikidata_entity().get_tag_ids(self,meaning_id,level)
    # #通过wikidata的id得到各个意向的标签
    #def get_wikidata_entity(self,wikidata_id):
    #    labels = get_wikidata_entity().get_property_by_wikidataid(wikidata_id)
    #    for i,j in labels:
    #        print i,j
    #    return
    ##通过许多词语id 得到 wikdiata的id
    #def get_meaning_ids_from_wordids(self,word_ids):
    #    meaning_ids = []
    #    for word_id in word_ids:
    #        meaning_ids.extend(self.get_meaning_ids(word_id))
    #    return meaning_ids
    ##通过词语id得到 wikdiata的id
    #def get_meaning_ids(self,word_id):
    #    wikidata_ids = get_wikidata_entity().get_wikidataid_by_wordid(word_id)
    #    return wikidata_ids
    ##通过名字得到词语的ID
    #def get_wordid(self,word_name):
    #    word_ids = get_word().get_wordid_by_wordname(word_name)
    #    return word_ids
if __name__ == '__main__':
    sftbw = Search_for_tags_by_word()
    print sftbw.run('公司')