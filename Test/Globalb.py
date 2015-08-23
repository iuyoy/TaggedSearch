#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#测试不同文件中的全局变量
from Globala import stack
def badd(str):
    stack.append(str)
    print 'b',stack
    