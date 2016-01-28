#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#Used for paper
import sys,os
sys.path.append(sys.path[0]+'/..')

from Global.db_op import Db_op as DB
from Global.config import *
from Global.global_function import *
import jieba
from gensim import corpora, models, similarities
prefix_data = "data/"
prefix_lsi = "lsi"
prefix_lda = "lda"
prefix_con = "all_"
#prefix_con = "main_"
prefix_tag = "tag_"
prefix_word = "word_"
postfix_dict = ".dict"
postfix_corpora = ".mm"
postfix_model = ".model"
prefix_website = "website"
class Search(object):
    search_words = set()
    search_tags = []
    websites = {}
    def __init__(self):
        self.db = DB(dbinfo = dbinfo)
        self.db.connect()
        super(Search, self).__init__()
    def search(self,search_sentence = ''):
        #self.search_sentence_op(search_sentence)
        self.search_words = set(('苹果','手机','苹果手机'))
        self.get_words()
        print self.search_words
        self.read_websites()
        self.get_tags()
        self.load()
        self.match()
    #查询句处理 处理
    def search_sentence_op(self,search_sentence):
        search_parts = search_sentence.split()
        for search_part in search_parts:
            self.search_words.add(search_part)
            for word in jieba.lcut_for_search(search_part):self.search_words.add(word) 
    #获取word的id
    def get_words(self,sign = 11):
        sql = "SELECT `id` FROM `"+wiki_db+"`.`"+words_table+"` WHERE `word_name`= %s AND sign = "+str(int(sign))
        self.search_words = [(word_name,self.db.fetchOneRow()[0] if self.db.select(sql,word_name) else 0) for word_name in self.search_words]
    #获取word的id
    def get_tags(self):
        sql = "SELECT `entity_id` FROM `wiki`.`word_tags` WHERE word_id = %s"
        for word in self.search_words :
            if word[1] != 0 and self.db.select(sql,word[1]):
               self.search_tags.extend([str(tag[0]) for tag in self.db.fetchAllRows()]) 
    def load(self):
        self.dictionary = corpora.Dictionary.load(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_dict)
        self.corpus = corpora.MmCorpus(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_corpora) # comes from the first tutorial, "From strings to vectors"
        print(self.corpus)
    def match(self):
        self.lsi()
    def lda(self):
        lda = models.LdaModel.load(prefix_data+prefix_con+prefix_tag+prefix_lda+postfix_model)
        #lda = models.LdaModel(self.corpus, id2word=self.dictionary, num_topics=30)
        vec_bow = self.dictionary.doc2bow(self.search_tags)
        print vec_bow
        vec_lda = lda[vec_bow] # convert the query to Lda space
        print(vec_lda)
        index = similarities.MatrixSimilarity(lda[self.corpus])
        sims = index[vec_lda]
        #print(list(enumerate(sims)))
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        
        print len(sims)
        for id,rank in sims:
            print id,self.websites[id],rank
    def lsi(self):
        lsi = models.LsiModel.load(prefix_data+prefix_con+prefix_tag+prefix_lsi+postfix_model)
        vec_bow = self.dictionary.doc2bow(self.search_tags)
        print vec_bow
        vec_lsi = lsi[vec_bow] # convert the query to lsi space
        print(vec_lsi)
        index = similarities.MatrixSimilarity(lsi[self.corpus])
        sims = index[vec_lsi]
        #print(list(enumerate(sims)))
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        
        print len(sims)
        for id,rank in sims:
            print id,self.websites[id],rank
    def read_websites(self):
        with open(prefix_data+prefix_con+prefix_website+".txt",'r') as fpw:
            for line in fpw:
                web = line.split()
                self.websites[int(web[0])] = web[1]
if __name__ == "__main__":
    ts = Search()
    ts.search("苹果手机")

