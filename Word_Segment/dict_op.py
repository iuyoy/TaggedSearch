#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

import sys,os
sys.path.append(sys.path[0]+'/..')
from Global.global_function import printout
#去重
def duplicate_removal(path):
    words = {}
    
    with open(path,'r') as ori_dict:
        line = 0
        for word in ori_dict:
            line += 1
            word = unicode(word,'utf-8')
            try:
                word_name,count,pos = word.split()
            except:
                printout(3,"pass word %d:%s" %(line,word))
            if word_name not in words:
                words[word_name]=(count,pos)
        with open(path+'_new','a') as new_dict:
            new_dict_content = ''
            line = 0
            for word,pro in words.items():
                try:
                    new_dict_content += word+' '+pro[0]+' '+pro[1]+'\n'
                except:
                    printout(4,"special word:%s",word)
                    new_dict_content += word.encode('utf-8')+' '+pro[0]+' '+pro[1]+'\n'
                line += 1
                if line % 10000 == 0 :
                    try:
                        new_dict.write(new_dict_content)
                    except:
                        new_dict.write(new_dict_content.encode('utf-8'))    
                    new_dict_content = ''
                    printout(5,"finish %d lines" %(line))
    return False

if __name__ == '__main__':
    dict_path = 'words.txt'
    duplicate_removal(dict_path)