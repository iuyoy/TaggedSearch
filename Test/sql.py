#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')

from Scripts.db_op import Db_op as DB
from Generate_Tags.ini import *
db = DB(dbinfo = dbinfo)


def query(id):
    sql = "SELECT value FROM test WHERE id = "+str(id)
    ret = db.select(sql)
    if ret>0:
        print ret,db.fetchOneRow()
    else:
        print ret,"select failed"

def insert(id,value):
    sql = 'INSERT INTO test(id,value) VALUES(%d,%d)' %(id,value)
    db.insert(sql)

def update(id,value):
    sql = 'UPDATE test SET value = %d WHERE id = %d' %(value,id)
    db.update(sql)

db.connect()
for i in range(10):
    insert(i,2)
    query(i)
    update(i,1)
    query(1)