#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append(sys.path[0]+'/..')

from Global.db_op import Db_op as DB
from Global.config import *
from Global.global_function import *
import jieba
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

prefix_data = "data/"
prefix_lsi = "lsi"
prefix_lda = "lda"
#prefix_con = "all_"
prefix_con = "main_"
prefix_tag = "tag_"
prefix_word = "word_"
postfix_dict = ".dict"
postfix_corpora = ".mm"
postfix_model = ".model"
prefix_website = "website"

class Search(object):
    #name:[id,rank]
    search_words = {}
    #id:[count,wiki_id,name,rank]
    l1_tags = {}
    #id:[count,wiki_id,name,rank]
    l2_tags = {}
    max_search_length = 30
    real_sentence = ''

    corpus=[]
    vec=[]
    num_features = 0
    result = []
    #id:[(vec_id,count)]
    websites = {}
    words_list = []
    tags_list = []
    
    def __init__(self,max_search_length = 30):
        super(Search, self).__init__()
        self.db = DB(dbinfo = dbinfo)
        self.db.connect()
    def do_lda(self,start = 1,limit = 1):
        self.get_lda_websites(start,limit)
        count = 0
        website_list = []
        with open(prefix_data+prefix_con+prefix_website+".txt",'w') as fpw:
            for web_id,url,title,content,sign in self.websites:
                self.get_words(web_id)
                ret = self.get_tags(web_id)
                if ret:
                    fpw.write("%s %s\n" %(count,web_id))
                    count += 1
        
        print len(self.websites),len(self.words_list),len(self.tags_list)
        self.word_dictionary = corpora.Dictionary(self.words_list)
        self.tag_dictionary = corpora.Dictionary(self.tags_list)
        self.word_corpus = [self.word_dictionary.doc2bow(words) for words in self.words_list]
        self.tag_corpus = [self.tag_dictionary.doc2bow(tags) for tags in self.tags_list]
        self.word_dictionary.save(prefix_data+prefix_con+prefix_word+prefix_lda+postfix_dict)
        self.tag_dictionary.save(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_dict)
        corpora.MmCorpus.save_corpus(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_corpora,self.tag_corpus)
        corpora.MmCorpus.save_corpus(prefix_data+prefix_con+prefix_word+prefix_lda+postfix_corpora,self.word_corpus)
        word_lda = models.LdaModel(self.word_corpus, id2word=self.word_dictionary, num_topics=30)
        word_lda.save(prefix_data+prefix_con+prefix_word+prefix_lda+postfix_model)
        tag_lda = models.LdaModel(self.tag_corpus, id2word=self.tag_dictionary, num_topics=30)
        tag_lda.save(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_model)
        word_lsi = models.LsiModel(self.word_corpus, id2word=self.word_dictionary, num_topics=30)
        word_lsi.save(prefix_data+prefix_con+prefix_word+prefix_lsi+postfix_model)
        tag_lsi = models.LsiModel(self.tag_corpus, id2word=self.tag_dictionary, num_topics=30)
        tag_lsi.save(prefix_data+prefix_con+prefix_tag+prefix_lsi+postfix_model)

    #得到一定的websites用于lda
    def get_lda_websites(self,start = 1,limit = 1):
        start = int(start)
        limit = int(limit)
        sql = "SELECT `id`,`url`,`title`,`content`,`sign` FROM `"+wiki_db+"`.`websites` WHERE id >= %s LIMIT %s"
        ret = self.db.select(sql,(start,limit))
        if ret:
            self.websites = self.db.fetchAllRows()
    def get_words(self,website_id):
        sql = "SELECT word_id,word_name,ww.count,w.sign FROM websites_words AS ww,words AS w WHERE ww.word_id = w.id AND ww.website_id = %s AND w.sign >2 "
        ret = self.db.select(sql,website_id)
        if ret:
            words = []
            for word_id,word_name,count,sign in self.db.fetchAllRows():
                #print word_id,word_name,count,sign
                for i in range(count):
                    words.append(str(word_id)) 
            self.words_list.append(words)
    def get_tags(self,website_id):
        sql = "SELECT\
                 entity_id,\
                sum(www.count) as count\
                FROM\
	            `wiki`.`word_tags` AS wwt,\
	                `wiki`.`websites_words` AS www,\
                  `wiki`.`entities` AS we,\
                `wiki`.`words` as ww\
                WHERE\
	                www.word_id = wwt.word_id \
                AND www.word_id = ww.id \
                AND wwt.entity_id = we.id \
                AND www.website_id = %s \
                AND we.sign = 1 \
                AND www.count>1 \
                AND ww.sign = 11\
                GROUP BY entity_id \
                HAVING count(entity_id)>1 \
                ORDER BY count DESC "
        ret = self.db.select(sql,website_id)
        if ret:
            tags = []
            for tag_id,count in self.db.fetchAllRows():
                # print tag_id,count,tag_name
                for i in range(count):
                    tags.append(str(tag_id)) 
            self.tags_list.append(tags)
        else:
            print website_id
            return False
        return True

def Similarity(dictionary,corpus):
    return      
if __name__ == '__main__':
    ss =Search()
    ss.do_lda(1,1001)
