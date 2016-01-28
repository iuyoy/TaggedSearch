#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append(sys.path[0]+'/..')

from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import *
dbinfo={\
'host' : 'localhost'\
,'user' : 'root'\
,'passwd' : 'root'\
,'db' : 'wiki'\
,'port' : 3306\
,'charset' : 'utf8'\
}
stop_words_file = 'D:\ROW\DChuan2015\mine_stopwords_v1.txt'
class insert_stopwords(object):
    db = DB(dbinfo = dbinfo)
    stop_words = set()
    def __init__(self):
        super(insert_stopwords,self).__init__()
        self.db.connect()
    def run(self):
        self.set_stop_words(stop_words_file)
        for stop_word in self.stop_words:
            self.insert_into_db(modify_charater(stop_word)) 
    def set_stop_words(self,stop_words = ''):
        words_type = type(stop_words)
        #str则当作路径
        if (words_type == str and stop_words != ''):
            try:
                with open(stop_words,'r') as stopwords:
                    self.stop_words |= set(stopwords.read().split())
                    return True
            except Exception,e:
                printout(0,e)
                return False
        elif(words_type == set):
            self.stop_words |= stop_words
            return True
        elif(words_type == list):
            self.stop_words |= set(stop_words)
            return True
        else:
            return False 
    def insert_into_db(self,stop_word):
        rs = self.check_stop_word(stop_word)
        if(rs):
            printout(2,"%s has inserted into db, then change it's sign." %(stop_word))
            word_id,pos,sign = rs
            if (sign == 0 or sign == 1):
                ret = self.change_sign(word_id)
                if (ret):
                    printout(2,"    Change %s's sign to 2 successfully." %(stop_word))
                    return True
        else:
            printout(2,"%s isn't inserted into db, then insert it into db." %(stop_word))
            sql = 'INSERT INTO `wiki`.`words`(`word_name`,`pos`,`sign`) VALUES(%s,%s,%s)'
            id = self.db.insert(sql,(stop_word,'stop',2))
            if (id):
                printout(2,"    Insert %s into db successfully." %(stop_word))
                return True
    def change_sign(self,word_id):
        sql = "UPDATE `wiki`.`words` SET sign = 2 WHERE id = %s "
        ret = self.db.update(sql,word_id)
        return ret
    def check_stop_word(self,stop_word):
        sql = "SELECT `id`,`pos`,`sign` FROM `wiki`.`words` WHERE `word_name` = %s"
        ret = self.db.select(sql,stop_word)
        if ret:
            return self.db.fetchOneRow()
        else:
            return False

if __name__ == "__main__":
    isw = insert_stopwords()
    isw.run()
    