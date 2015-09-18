#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append('..')
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

class Get_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Get_data, self).__init__()
        self.connect()
    def connect(self):
        try:
            self.db.connect()
        except:
            pass
    def __delete__(self):
        try:
            self.db.close()
        except:
            pass

class Get_web(Get_data):
    def __init__(self):
        super(Get_web, self).__init__()

    def get_one_cnbeta_article(self , id = 0):
        id = int(id)
        if (id == 0):
            sql = "SELECT id,title,content FROM `%s`.`%s` WHERE `level` = 0 AND id > 53000 LIMIT 1  " %(search_db,cnbeta_table)
        else:
            sql = "SELECT id,title,content FROM `%s`.`%s` WHERE `level` = 0 AND id = %d" %(search_db,cnbeta_table,id)
        result = self.db.select(sql)
        if(result):
            return self.db.fetchOneRow()
        else:
            return []