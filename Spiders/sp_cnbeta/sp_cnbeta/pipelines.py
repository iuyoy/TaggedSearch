# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class SpCnbetaPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '23.244.180.241',
            port = 3306,
            db = 'search',
            user = 'search',
            passwd = 'search&Tagged',
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = False)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item
    def _conditional_insert(self ,tx ,item):
        tx.execute("select id from sp_cnbeta where id = %s", (item['id'][0], ))
        result = tx.fetchone()
        if (result and len(item['id'])>0):
            print ("Item %d has been already stored in db, or it doesn't have any id info." % item['id'][0])
        else:
            content = ''
            picture = 0
            media = 0
            for i in item:
                if(i=='content'):
                    for j in item['content']:
                        content += j
                elif(i=='picture' and len(item[i])>0):
                    picture = 1
                elif(i=='media' and len(item[i])>0):
                    media = 1
                else:
                    if(item[i]==[]):
                        item[i].append('空缺')
            try:    
                sql = '''INSERT INTO sp_cnbeta (\
id,url,title,date,author_name,author_url,content,picture,media,level)\
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                #sql = '''insert into sp_cnbeta (id,url,title,date,author_name,author_url,content,picture,media,level)values(?,?,?,?,?,?,?,?,?,?,?)'''
                
                #print tx.execute("INSERT INTO sp_cnbeta (id) VALUES(%d)",(1,))
                if (tx.execute(sql,(item['id'][0],item['url'][0],item['title'][0],item['date'][0],item['author_name'][0],item['author_url'][0],content,picture,media,0,))):
                    print ("Save item %d successfully" %(item['id'][0]))
            except:
                print ("Something wrong @SpCnbetaPipeline")
            
            #log.msg("Item stored in db: %s" % item, level=log.DEBUG)
