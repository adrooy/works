#! -*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^iplay_mgmt/game/$', 'game.views.index', name='game'),
    url(r'^iplay_mgmt/game/detail/$', 'game.views.detail', name='detail'),
    url(r'^iplay_mgmt/game/channel/$', 'game.views.channel', name='channel'),
    url(r'^iplay_mgmt/game/gameinfo/$', 'game.views.game_info', name='game_info'),
    url(r'^iplay_mgmt/game/labelinfo/$', 'game.views.label_info', name='label_info'),
    url(r'^iplay_mgmt/game/search/$', 'game.views.search', name='search'),
    url(r'^iplay_mgmt/game/label_info_change/$', 'game.views.label_info_change', name='label_info_change'),
    url(r'^iplay_mgmt/game/addScreen/$', 'game.views.addScreen', name='addScreen'),
)
