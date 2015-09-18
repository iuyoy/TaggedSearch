#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#from:整理：兔大侠和他的朋友们（http://www.tudaxia.com）
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
    def __init__(self,host = 'localhost',user = 'root',passwd = 'root',db = 'test',port = 3306,charset = 'utf8',dbinfo = None):
        super(Db_op,self).__init__()
        if (dbinfo != None):
            self.host = dbinfo['host']
            self.user = dbinfo['user']
            self.passwd = dbinfo['passwd']
            self.db = dbinfo['db']
            self.port = dbinfo['port']
            self.charset = dbinfo['charset']
        else:
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
            self.cur.execute("SET NAMES "+self.charset)
            self.conn.commit()
            return True
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return False
    
    #执行 SELECT 语句
    def select(self,sql,para = ''):
        try:
            if (para == ''):
                result = self.cur.execute(sql)
            else:
                result = self.cur.execute(sql,para)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            result = False
        return result
    #执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
    def insert(self,sql,para = ''):
        try:
            if (para == ''):
                self.cur.execute(sql)
            else:
                self.cur.execute(sql,para)
            result = self.conn.insert_id()
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            result = False
        return result
    def insert_list(self,sql,para_list):
        try:
            result = self.cur.executemany(sql,para_list)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            result = False
        return result
    #执行 UPDATE 及 DELETE 语句
    def update(self,sql,para = ''):
        try:
            if (para == ''):
               result =  self.cur.execute(sql)
            else:
               result =  self.cur.execute(sql,para)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            result = False
        return result
    #SQL过滤
    def SQL_filter(self,content):
        return MySQLdb.escape_string(content)
    #返回结果列表
    def fetchAllRows(self):
        return self.cur.fetchall()
    #返回结果列表，并将嵌套的list变成一个list，用于只有一列的情况
    def fetchAllRowsOneList(self):
        result = []
        for line in self.cur.fetchall():
            result.append(line[0])
        return result
    #返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
    def fetchOneRow(self):
        return self.cur.fetchone()
    #获取结果行数
    def getRowCount(self):
        return self.cur.rowcount

    def close(self):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1]) 
    def __del__(self):
        self.close()

if __name__ == '__main__':
    dp = Db_op()
    dp.connect()