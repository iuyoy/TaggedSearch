#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#测试不同文件中的全局变量
import sys,os
sys.path.append('..')
from Globalb import badd 
from Globalc import cadd 
from Globala import stack
def dadd(str):
    stack.append(str)
    print 'd',stack

if __name__ == '__main__':
    dadd('d')
    badd('b')
    cadd('c')
    print stack