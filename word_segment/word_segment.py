#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import jieba

def default_test():
    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式

    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print(", ".join(seg_list))

    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print(", ".join(seg_list))

def test2():
    import jieba.posseg as pseg
    words = pseg.cut("电视广播有限公司")
    for word, flag in words:
        print('%s %s' % (word, flag))

def test(string,cut_all=False):
    seg_list = jieba.cut(string, cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#test('结论:从整体测试结果上看，分词速度以及文本超过一定长度的性能测试未进行，自定义词典也是一个很大的影响分词因素，也未涵盖测试，排除以上两点,整体上看，对繁体以及网址的分词，中科院的分词系统做到最好，如果论说对容易歧义的文本，结巴不错，这两者也相对功能方面会更丰富。感觉如果python分词，建议使用结巴或者中科院分词调用C库使用,如果担心调用C库等产生的相关问题，可以使用结巴分词系统，是个不错的选择，在分词前进行简繁转换；或者采用中科院的分词，加上自定义词典，也是不错的选择，不过就本人在python调用C库使用中科院分词的过程中，存在用户自定义词典导入会过于优先（如导入用户词典，中信，当分词内容[我们中信仰佛教的人]会分词成[我们,中信,仰,佛教,的,人]）以及存在导入失败情况，还有函数调用安全问题。主要是根据需要进行选择不同的分词。有空再进行性能测试！')
test("电视广播有限公司",False)
test("电视广播有限公司",True)