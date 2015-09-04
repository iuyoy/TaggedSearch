#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
from Generate_Tags.ini import *
class search_for_tags_by_words(object):
    def __init__(self):
        super(search_for_tags, self).__init__()
    def run(self):
        return
    
class search_fro_tags_by_word(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(search_fro_tags_by_word, self).__init__()
        self.db.connect()
    def run(self):
        return 0
    def get_wordid(self,word_name):
        sql = ''