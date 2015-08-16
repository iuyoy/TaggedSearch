#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import MySQLdb
class Db_op(object):
    host = 'localhost'
    user = 'root'
    passwd = 'root'
    db = 'test'
    port = 3306
    charset = 'utf8'
    conn = None
    cur = None
    def __init__(self,host = 'localhost',user = 'root',passwd = 'root',db = 'test',port = 3306,charset = 'utf8'):
        super(Db_op,self).__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        
    def connect(self):
        try:
            self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.charset)
            self.cur = self.conn.cursor()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
    def insert(self,sql):
        try:
            self.cur.execute("SET NAMES "+self.charset)
            self.cur.execute(sql)
            insert_id = self.conn.insert_id()
            self.conn.commit()
            return insert_id
            
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return False
    #SQL过滤
    def SQL_filter(self,content):
        return MySQLdb.escape_string(content)

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1]) 
    def __del__(self):
        self.close()
