#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Word_Segment.word_segment import *
from get_data import *

class get_website(object):
    def run(self,id = 0):
        self.get_article(id)
    #得到文章
    def get_article(self,id = 0):
        article = Get_article().get_one_cnbeta_article(id)
        return article
    #article 结构[id,title,content]

if __name__ == "__main__":
    gw = get_website()
    gw.run()