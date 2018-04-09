#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 15:44
# @Author  : hearecho
# @Site    :
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('update_comment',views.update_comment,name='update'),
]