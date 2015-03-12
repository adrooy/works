#coding=utf-8


__author__ = 'xiangxiaowei'


from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username=forms.CharField(label=_(u"昵称"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"密码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    
