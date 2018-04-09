#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 16:30
# @Author  : hearecho
# @Site    : 
# @File    : deal_error.py
# @Software: PyCharm
from django.shortcuts import render

def deal_error(request,message):
    return render(request,'error.html',{'message':message})