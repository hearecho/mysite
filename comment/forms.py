#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 17:37
# @Author  : hearecho
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):#验证
#         验证用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError("用户尚未登陆")

#         评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']


        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
           raise forms.ValidationError("评论对象不存在")
        return self.cleaned_data



