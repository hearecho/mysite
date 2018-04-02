#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 20:16
# @Author  : hearecho
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import datetime
from blog.models import Blog
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum,ReadDetail


def read_count_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = 'blog_{}_readed'.format(obj.id)
    if not request.COOKIES.get(key):
        readnum ,created= ReadNum.objects.get_or_create(content_type=ct,object_id=obj.id)

        readnum.read_num += 1
        readnum.save()

        date = timezone.now()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id,date=date)
        readDetail.read_num += 1
        readDetail.save()

        return key

def get_seven_readNum(contentType):
    today = timezone.now().date()
    read_nums = []
    dates=[]
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        readDetails = ReadDetail.objects.filter(content_type=contentType,date=date)
        result = readDetails.aggregate(read_num_sum = Sum('read_num'))#返回字典  {'read_num_sum':'0'}
        read_nums.append(result['read_num_sum'] or 0)

    return dates,read_nums

def get_today_hot_data(contentType):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=contentType,date=today).order_by('-read_num')
    return read_details[:7]

def get_yseterday_hot_data(contentType):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=contentType, date=yesterday).order_by('-read_num')
    return read_details[:7]


def get_week_hot_date():
    today =  timezone.now().date()
    date = today - datetime.timedelta(days=7)
#     分类统计  避免一篇博客重复占用
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gt=date)\
                            .values('id','title',)\
                            .annotate(read_num_sum = Sum("read_details__read_num"))\
                            .order_by("-read_num_sum")
    return blogs[:7]

def get_month_hot_date():
    today =  timezone.now().date()
    date = today - datetime.timedelta(days=30)
#     分类统计  避免一篇博客重复占用
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gt=date)\
                            .values('id','title',)\
                            .annotate(read_num_sum = Sum("read_details__read_num"))\
                            .order_by("-read_num_sum")
    return blogs[:7]
