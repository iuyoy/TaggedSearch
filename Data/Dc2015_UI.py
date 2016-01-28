# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dc2015_classify_doc.ui'
#
# Created: Tue Jan 26 22:08:27 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(688, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.content = QtGui.QTextBrowser(self.centralwidget)
        self.content.setGeometry(QtCore.QRect(0, 60, 441, 521))
        self.content.setObjectName(_fromUtf8("content"))
        self.title = QtGui.QTextBrowser(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(0, 10, 441, 41))
        self.title.setObjectName(_fromUtf8("title"))
        self.id = QtGui.QTextEdit(self.centralwidget)
        self.id.setGeometry(QtCore.QRect(460, 120, 91, 41))
        self.id.setObjectName(_fromUtf8("id"))
        self.Jump = QtGui.QPushButton(self.centralwidget)
        self.Jump.setGeometry(QtCore.QRect(560, 120, 91, 41))
        self.Jump.setObjectName(_fromUtf8("Jump"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 220, 91, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(460, 280, 91, 51))
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.pushButton3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(460, 340, 91, 51))
        self.pushButton3.setObjectName(_fromUtf8("pushButton3"))
        self.pushButton4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton4.setGeometry(QtCore.QRect(560, 220, 91, 51))
        self.pushButton4.setObjectName(_fromUtf8("pushButton4"))
        self.pushButton5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton5.setGeometry(QtCore.QRect(560, 280, 91, 51))
        self.pushButton5.setObjectName(_fromUtf8("pushButton5"))
        self.pushButton6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton6.setGeometry(QtCore.QRect(560, 340, 91, 51))
        self.pushButton6.setObjectName(_fromUtf8("pushButton6"))
        self.pushButton7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton7.setGeometry(QtCore.QRect(560, 400, 91, 51))
        self.pushButton7.setObjectName(_fromUtf8("pushButton7"))
        self.pushButton8 = QtGui.QPushButton(self.centralwidget)
        self.pushButton8.setGeometry(QtCore.QRect(460, 400, 91, 51))
        self.pushButton8.setObjectName(_fromUtf8("pushButton8"))
        self.pushButton9 = QtGui.QPushButton(self.centralwidget)
        self.pushButton9.setGeometry(QtCore.QRect(460, 460, 91, 51))
        self.pushButton9.setObjectName(_fromUtf8("pushButton9"))
        self.pushButton10 = QtGui.QPushButton(self.centralwidget)
        self.pushButton10.setGeometry(QtCore.QRect(560, 460, 91, 51))
        self.pushButton10.setObjectName(_fromUtf8("pushButton10"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.content, self.title)
        MainWindow.setTabOrder(self.title, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.id)
        MainWindow.setTabOrder(self.id, self.Jump)
        MainWindow.setTabOrder(self.Jump, self.pushButton3)
        MainWindow.setTabOrder(self.pushButton3, self.pushButton2)
        MainWindow.setTabOrder(self.pushButton2, self.pushButton4)
        MainWindow.setTabOrder(self.pushButton4, self.pushButton5)
        MainWindow.setTabOrder(self.pushButton5, self.pushButton6)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "毫无关系", None))
        self.content.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">网页内容</p></body></html>", None))
        self.title.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">标题</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.id.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ID</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.Jump.setText(_translate("MainWindow", "Jump", None))
        self.pushButton3.setText(_translate("MainWindow", "苹果 手机", None))
        self.pushButton2.setText(_translate("MainWindow", "苹果 水果", None))
        self.pushButton4.setText(_translate("MainWindow", "ALL", None))
        self.pushButton5.setText(_translate("MainWindow", "水果", None))
        self.pushButton6.setText(_translate("MainWindow", "手机", None))
        self.pushButton7.setText(_translate("MainWindow", "Both", None))
        self.pushButton8.setText(_translate("MainWindow", "一点 手机", None))
        self.pushButton9.setText(_translate("MainWindow", "一点 水果", None))
        self.pushButton10.setText(_translate("MainWindow", "both little", None))

