﻿#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append(sys.path[0]+'/..')

from Global.db_op import Db_op as DB
from Global.config import *
from Global.global_function import *
import jieba
from gensim import corpora, models, similarities

class Search(object):
    #name:id
    search_words = {}
    #id:[count,wiki_id,name]
    l1_tags = {}
    #id:[count,wiki_id,name]
    l2_tags = {}
    max_search_length = 30
    real_sentence = ''

    corpus=[]
    vec=[]
    num_features = 0
    result = []
    #id:[(vec_id,count)]
    websites = {}
    def __init__(self,max_search_length = 30):
        super(Search, self).__init__()
        self.max_search_length = max_search_length
        self.db = DB(dbinfo = dbinfo)
        self.db.connect()
    def run(self,search_sentence):
        print len(search_sentence),search_sentence
        self.search_sentence_op(search_sentence)
        return words

    def search_sentence_op(self,search_sentence):
        self.clear()
        is_tool_long = self.sentence_segment(search_sentence)
        self.get_words()
        self.get_tags()
        self.get_deep_tags()
        self.set_gensim()
        webs = self.get_websites()
        return (self.search_words,self.l1_tags,self.l2_tags,webs)

    def set_gensim(self):
        for name,word_id in self.search_words.items():
            self.vec.append([self.num_features,1.0])
            self.search_websites_by_word(word_id)
            self.num_features += 1
        #for tag_id in self.l1_tags:
        #    self.vec.append([self.num_features,1.0])
        #    self.search_websites_by_tag(tag_id)
        #    self.num_features += 1
        for tag_id in self.l2_tags:
            self.vec.append([self.num_features,1.0])
            self.search_websites_by_tag(tag_id)
            self.num_features += 1
        self.corpus = list(self.websites.itervalues())
        self.websites = list(self.websites.iterkeys())
        tfidf = models.TfidfModel(self.corpus)
        index = similarities.SparseMatrixSimilarity(tfidf[self.corpus], num_features=self.num_features)
        sims = index[tfidf[self.vec]]
        self.result = sorted(enumerate(sims), key=lambda e:e[1], reverse=True)
        
    def get_websites(self,page = 1,npp=10):
        webs = {'page':page,'npp':0,'total':len(self.websites)}
        if (type(self.websites) == list):
            for index in xrange((page-1)*npp,page*npp):
                ret = self.get_website(self.websites[self.result[index][0]])
                if ret:
                    print index-(page-1)*npp
                    webs[index-(page-1)*npp] = ret
                else:
                    break
            webs['npp'] = index-(page-1)*npp+1
        return webs
    def get_website(self,page_id):
        sql = "SELECT `url`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+"` WHERE id = %s"
        ret = self.db.select(sql,page_id)
        if ret:
            return self.db.fetchOneRow()
        return False
    def search_websites_by_word(self,word_id):
        sql = "SELECT `website_id`,`count`,`sign` FROM `"+wiki_db+"`.`"+websites_words_table+"` WHERE word_id = %s"
        ret = self.db.select(sql,word_id)
        if ret:
            for website,count,sign in self.db.fetchAllRows():
                if website in self.websites:
                    #id:[(vec_id,count)]
                    self.websites[website].append((self.num_features,count))
                else:
                    self.websites[website]=[(self.num_features,count)]
    def search_websites_by_tag(self,tag_id):
        sql = "SELECT `website_id`,`count`,`sign` FROM `"+wiki_db+"`.`"+websites_tags_table+"` WHERE entity_id = %s"
        ret = self.db.select(sql,tag_id)
        if ret:
            for website,count,sign in self.db.fetchAllRows():
                if website in self.websites:
                    #id:[(vec_id,count)]
                    self.websites[website].append((self.num_features,count))
                else:
                    self.websites[website]=[(self.num_features,count)]
    #分词
    def sentence_segment(self,search_sentence):
        search_sentence = modify_charater(search_sentence)
        search_sentence = search_sentence.split()
        search_length = 0
        self.real_sentence = ''
        for fragment in search_sentence:
            search_length += len(fragment)
            if search_length > self.max_search_length:
                fragment = fragment[:self.max_search_length+len(fragment)-search_length]
                self.real_sentence += fragment+' '
            for word in jieba.lcut_for_search(fragment):
                if word not in self.search_words:
                    self.search_words[word] = 0
            if search_length > self.max_search_length:
                return True
        return False
    def get_words(self):
        sql = "SELECT `id` FROM `wiki`.`words` WHERE `word_name`=%s"
        for word in self.search_words:
            ret = self.db.select(sql,word)
            if ret:
                id = self.db.fetchOneRow()
                self.search_words[word] = id
        printout(0,"uesd words number:%d" %(len(self.search_words)))

    def get_tags(self):
        sql = "SELECT we.`id`,we.`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) AS `name` \
        FROM `wiki`.`entities` AS we,`wiki`.`word_entity` AS wwe \
        WHERE wwe.`entity_id` = we.`id` AND wwe.`word_id` = %s"
        for word_id in self.search_words.itervalues():
            ret = self.db.select(sql,word_id)
            if ret:
                result = self.db.fetchAllRows()
                for tag_id,wikidata_id,name in result:
                    if tag_id not in self.l1_tags:
                        self.l1_tags[tag_id] = [1,wikidata_id,name]
                    else:
                        self.l1_tags[tag_id][0] += 1
        printout(0,"uesd l1 self.l1_tags number:%d" %(len(self.l1_tags)))

    def get_deep_tags(self):
        sql = "SELECT we.`id`,`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
AS `name`,`property_name` AS property,count(we.id) AS `count` \
FROM wiki.entities AS we,wiki.entity_properties AS wep \
WHERE we.wikidata_id = wep.property_value AND wep.entity_id = %s GROUP BY id \
ORDER BY `count` DESC;"
        for tag_id in self.l1_tags:
            ret = self.db.select(sql,tag_id)
            if ret:
                result = self.db.fetchAllRows()
                for tag_id,wikidata_id,name,property,count in result:
                    if tag_id not in self.l2_tags:
                        self.l2_tags[tag_id] = [count,wikidata_id,name]
                    else:
                        self.l2_tags[tag_id][0] += count

    def clear(self):
        self.search_words = {}
        self.l1_tags = {}
        self.l2_tags = {}
        self.vec = []
        self.corpus = []
        self.num_features = 0

if __name__ == '__main__':
    search_sentence = u"陆军"
    sh = Search()
    sh.search_sentence_op(search_sentence)
