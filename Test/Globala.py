#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
#测试不同文件中的全局变量
global stack
stack = []

def add(str):
    stack.append(str)
def show():
    print stack


