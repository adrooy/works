#! -*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'permission.views.page', name='index'),
    url(r'^permission/selected/$', 'permission.views.selected', name='selected'),
    url(r'^permission/is_finished/$', 'permission.views.is_finished', name='is_finished'),
    url(r'^permission/is_approved/$', 'permission.views.is_approved', name='is_approved'),
    url(r'^permission/not_approved/$', 'permission.views.not_approved', name='not_approved'),
    url(r'^permission/is_pending/$', 'permission.views.is_pending', name='is_pending'),
    url(r'^permission/downloadApk/$', 'permission.views.downloadApk', name='downloadApk'),
    url(r'^permission/checkApk/$', 'permission.views.checkApk', name='checkApk'),
    url(r'^permission/page/$', 'permission.views.page', name=''),
)
