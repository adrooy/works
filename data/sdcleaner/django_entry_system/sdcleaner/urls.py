#! -*- coding:utf-8 -*-


__author__ = 'zz'


from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^sdcleaner/$', 'sdcleaner.handler.page', name='sdcleaner index'),
    url(r'^sdcleaner/page/$', 'sdcleaner.handler.page', name='sdcleaner page'),
    url(r'^sdcleaner/selected/$', 'sdcleaner.handler.selected', name='sdcleaner selected'),
    url(r'^sdcleaner/download/$', 'sdcleaner.handler.download', name='sdcleaner download'),
    url(r'^sdcleaner/save/$', 'sdcleaner.handler.save', name='sdcleaner save'),
    url(r'^sdcleaner/approve/$', 'sdcleaner.handler.approve', name='sdcleaner approve'),
    url(r'^sdcleaner/disapprove/$', 'sdcleaner.handler.disapprove', name='sdcleaner disapprove'),
    url(r'^sdcleaner/pend/$', 'sdcleaner.handler.pend', name='sdcleaner pend'),
)
