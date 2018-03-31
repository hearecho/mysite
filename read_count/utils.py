#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 20:16
# @Author  : hearecho
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import datetime
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
        result = readDetails.aggregate(read_num_sum = Sum('read_num'))#返回字典
        read_nums.append(result['read_num_sum'] or 0)

    return dates,read_nums