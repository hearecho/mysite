#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 20:31
# @Author  : hearecho
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",widget=forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label="密码",widget=forms.PasswordInput(
                attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError("用户名不正确")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label="用户名",min_length=3,max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    email = forms.EmailField(label="邮箱",required=False,widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password = forms.CharField(label="密码",min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label="在输入密码", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再输入密码'}))


    #处理数据
    def clean_usernaem(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已经存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and email != "":
            raise forms.ValidationError("邮箱已经存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        print(self.cleaned_data)
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError("两次输入密码不一致")

        return password_again

