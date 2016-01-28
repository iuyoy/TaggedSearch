#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

def generate_stopswords_list(filename = "mine_stopwords.txt"):
    stopwords_list1 = """`1234567890-=~!@#$%^&*()_+qwertyuiop[]\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>? """
    stopwords_list2 = u"""｀１２３４５６７８９０－＝～！＠＃＄％＾＆＊（）＿＋ｑｗｅｒｔｙｕｉｏｐ［］＼｜｝｛ＰＯＩＵＹＴＲＥＷＱａｓｄｆｇｈｊｋｌ；＇ＡＳＤＦＧＨＪＫＬ：＂ｚｘｃｖｂｎｍ，．／？＞＜ＭＮＢＶＣＸＺ"""
    print len(stopwords_list1)
    print len(stopwords_list2)
    with open(filename,'w') as fp:
        content = ''
        for i in stopwords_list1:
            content += i+'\n'
        for i in stopwords_list2:
            content += i+'\n'
        fp.write(content.encode('utf8'))
            
    
if __name__ == '__main__':
    generate_stopswords_list()
