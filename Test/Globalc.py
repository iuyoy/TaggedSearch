#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#测试不同文件中的全局变量
from Globala import stack
from Globalb import *

def cadd(str):
    stack.append(str)
    print 'c',stack

