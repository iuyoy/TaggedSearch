#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
import string
sys.path.append(sys.path[0]+'/..')
from Global.db_op import Db_op as DB
from Global.config import *

from PyQt4 import QtGui,QtCore   
import Dc2015_UI  
from Dc2015_UI import _fromUtf8,_translate
class Classify_doc(QtGui.QMainWindow,Dc2015_UI.Ui_MainWindow):  
    db = DB(dbinfo = dbinfo)
    cur_id = 0
    def __init__(self,parent=None):  
        super(Classify_doc,self).__init__(parent)  
        self.db.connect()
        self.setupUi(self)  
        self.init_bottons()
        self.init_doc()
    def init_bottons(self):
        self.connect( self.Jump, QtCore.SIGNAL( 'clicked()' ), self.jump)
        self.connect( self.pushButton, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(1) )
        self.connect( self.pushButton2, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(2) )
        self.connect( self.pushButton3, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(3) )
        self.connect( self.pushButton4, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(4) )
        self.connect( self.pushButton5, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(5) )
        self.connect( self.pushButton6, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(6) )
        self.connect( self.pushButton7, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(7) )
        self.connect( self.pushButton8, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(8) )
        self.connect( self.pushButton9, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(9) )
        self.connect( self.pushButton10, QtCore.SIGNAL( 'clicked()' ), lambda: self.update_no(10) )
    def init_doc(self):
        sql = u"SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+wiki_db+"`.`websites` WHERE `sign` = 0 LIMIT 1"
        result = self.db.select(sql)
        if(result):
            self.cur_id,url,docno,title,content,self.sign = self.db.fetchOneRow()
            self.set_doc(self.cur_id,title,content)
        else:
            print ("Error:Can't init doc.")
            return False
    def next_doc(self):
        self.init_doc()
    def jump(self):
        num = int(self.id.toPlainText())
        sql = u"SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `"+wiki_db+"`.`websites` WHERE `id` = %s LIMIT 1"
        result = self.db.select(sql,num)
        if(result):
            self.cur_id,url,docno,title,content,self.sign = self.db.fetchOneRow()
            self.set_doc(self.cur_id,title,content)
        else:
            print("Error:Can't jump to %d") %(self.cur_id)
            sys.exit(-1)
    def update_no(self,num = 0):
        print self.cur_id,num
        sql = "UPDATE `wiki`.`websites` SET `sign`='%s' WHERE (`id`='%s')"
        para = (num,self.cur_id)
        ret = self.db.update(sql,para)
        if ret or int(self.sign) == int(num):
            self.next_doc()
        else:
            print("Error:Can't update sign @ %d") %(self.cur_id)
            sys.exit(-1)
    def set_doc(self,id,title,content):
        self.title.setText(_translate("MainWindow",title,None))
        self.content.setText(_translate("MainWindow",content,None))
        self.id.setText(_translate("MainWindow",str(id),None))
app=QtGui.QApplication(sys.argv)  
dialog=Classify_doc()  
dialog.show()  
app.exec_() 