#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
import string
sys.path.append(sys.path[0]+'/..')
from Global.db_op import Db_op as DB
from Global.config import *

#trantab = {}
#from_str = u'１２３４５６７８９０ｑｗｅｒｔｙｕｉｏｐａｓｄｆｇｈｊｋｌｚｘｃｖｂｎｍＱＷＥＲＴＹＵＩＯＰＡＳＤＦＧＨＪＫＬＺＸＣＶＢＮＭ'
#to_str = u'1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
#for i in range(len(from_str)):
#    trantab[ord(from_str[i])]=to_str[i]
#print trantab
trantab = {65296: u'0', 65297: u'1', 65298: u'2', 65299: u'3', 65300: u'4', 65301: u'5', 65302: u'6', 65303: u'7', 65304: u'8', 65305: u'9', 65313: u'A', 65314: u'B', 65315: u'C', 65316: u'D', 65317: u'E', 65318: u'F', 65319: u'G', 65320: u'H', 65321: u'I', 65322: u'J', 65323: u'K', 65324: u'L', 65325: u'M', 65326: u'N', 65327: u'O', 65328: u'P', 65329: u'Q', 65330: u'R', 65331: u'S', 65332: u'T', 65333: u'U', 65334: u'V', 65335: u'W', 65336: u'X', 65337: u'Y', 65338: u'Z', 65345: u'a', 65346: u'b', 65347: u'c', 65348: u'd', 65349: u'e', 65350: u'f', 65351: u'g', 65352: u'h', 65353: u'i', 65354: u'j', 65355: u'k', 65356: u'l', 65357: u'm', 65358: u'n', 65359: u'o', 65360: u'p', 65361: u'q', 65362: u'r', 65363: u's', 65364: u't', 65365: u'u', 65366: u'v', 65367: u'w', 65368: u'x', 65369: u'y', 65370: u'z'}
#print unicode(u'１２').translate(trantab)
db = DB(dbinfo = dbinfo)
db.connect()

def get_sogou_news(keywords,num,sign):
    sql = u"SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+\
        "` WHERE `content` like '%"+keywords+"%' AND `sign` = "+str(sign)+" LIMIT " +str(num)
    print u'查询'+keywords,sql
    result = db.select(sql)
    if(result):
        return db.fetchAllRows()
    else:
        return []
def insert_new_news(url,docno,title,content,sign,id=0):
    if id !=0:
        sql = u"INSERT INTO `wiki`.`websites_sogou` (`id`,`url`, `docno`, `title`, `content`, `sign`) VALUES (%s,%s, %s, %s, %s, %s);"
        ret = db.insert(sql,(id,url,docno,title,content,sign))
    else:
        sql = u"INSERT INTO `wiki`.`websites_sogou` (`url`, `docno`, `title`, `content`, `sign`) VALUES (%s, %s, %s, %s, %s);"
        ret = db.insert(sql,(url,docno,title,content,sign))
    if not ret:
        print "error"
        return

def add_apple():
    keywords = u'苹果'
    num = 500
    sign = 0
    ret = get_sogou_news(keywords,num,sign)
    if ret:
        for line in ret:
            id,url,docno,title,content,sign = line
            title = title.translate(trantab)
            content = content.translate(trantab)
            insert_new_news(url,docno,title,content,1)
def save_source(no = 400,max_num = 500):
    id = no
    num = 0
    while(True):    
        sql = u"SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+\
        "` WHERE `id` = "+str(id)+" AND `sign` = 0"
        db.select(sql)
        ret = db.fetchAllRows()
        if ret:
            id,url,docno,title,content,sign = ret[0]
            if u'苹果' not in content:
                #document = u'<id>'+str(id)+u'</id>\n'\
                #+u'<url>'+url+u'</url>\n'\
                #+u'<docno>'+docno+u'</docno>\n'\
                #+u'<title>'+title+u'</title>\n'\
                #+u'<content>'+content.translate(trantab)+u'</content>\n'\
                #+u'<sign>'+str(sign)+u'</sign>\n'
                #fp = open('data/source/'+str(id)+'.txt','w')
                #document=document.encode('utf8')
                title = title.translate(trantab)
                content = content.translate(trantab)
                insert_new_news(url,docno,title,content,0)
                num += 1
            else:
                print id,content
            id += 1000
            if num == max_num:
                return
save_source()
add_apple()
