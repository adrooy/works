#! -*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^iplay_mgmt/$', 'market.topic.index', name='index topic'),
    url(r'^iplay_mgmt/market/topic/$', 'market.topic.index', name='index topic'),
    url(r'^iplay_mgmt/market/topic_add/$', 'market.topic.add', name='add topic'),
    url(r'^iplay_mgmt/market/topic_alter/$', 'market.topic.alter', name='alter topic'),
    url(r'^iplay_mgmt/market/topic_edit/$', 'market.topic.edit', name='edit topic'),
    url(r'^iplay_mgmt/market/topic_delete/$', 'market.topic.delete', name='delete topic'),
    url(r'^iplay_mgmt/market/topic_isenabled/$', 'market.topic.isenabled', name='isenabled topic'),
    url(r'^iplay_mgmt/market/topic_notenabled/$', 'market.topic.notenabled', name='notenabled topic'),
    url(r'^iplay_mgmt/market/topic_up/$', 'market.topic.up', name='up topic'),
    url(r'^iplay_mgmt/market/topic_down/$', 'market.topic.down', name='down topic'),
    url(r'^iplay_mgmt/market/topic_move/$', 'market.topic.move', name='move topic'),
    url(r'^iplay_mgmt/market/topic_moveGame/$', 'market.topic.moveGame', name='moveGame topic'),
    url(r'^iplay_mgmt/market/topic_addGame/$', 'market.topic.addGame', name='addGame topic'),
    url(r'^iplay_mgmt/market/topic_delGame/$', 'market.topic.delGame', name='delGame topic'),
    url(r'^iplay_mgmt/market/topic_upGame/$', 'market.topic.upGame', name='upGame topic'),
    url(r'^iplay_mgmt/market/topic_downGame/$', 'market.topic.downGame', name='downGame topic'),
    url(r'^iplay_mgmt/market/recommend/$', 'market.recommend.index', name='index recommend'),
    url(r'^iplay_mgmt/market/recommend_addGame/$', 'market.recommend.addGame', name='addGame recommend'),
    url(r'^iplay_mgmt/market/recommend_delGame/$', 'market.recommend.delGame', name='delGame recommend'),
    url(r'^iplay_mgmt/market/recommend_upGame/$', 'market.recommend.upGame', name='upGame recommend'),
    url(r'^iplay_mgmt/market/recommend_moveGame/$', 'market.recommend.moveGame', name='moveGame recommend'),
    url(r'^iplay_mgmt/market/recommend_downGame/$', 'market.recommend.downGame', name='downGame recommend'),
    url(r'^iplay_mgmt/market/recommend_addBanner/$', 'market.recommend.addBanner', name='addBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_alterBanner/$', 'market.recommend.alterBanner', name='alterBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_editBanner/$', 'market.recommend.editBanner', name='editBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_moveBanner/$', 'market.recommend.moveBanner', name='moveBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_upBanner/$', 'market.recommend.upBanner', name='upBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_downBanner/$', 'market.recommend.downBanner', name='downBanner recommend'),
    url(r'^iplay_mgmt/market/recommend_isenabledBanner/$', 'market.recommend.isenabledBanner', name='isenabled banner'),
    url(r'^iplay_mgmt/market/recommend_notenabledBanner/$', 'market.recommend.notenabledBanner', name='notenabled banner'),
    url(r'^iplay_mgmt/market/recommend_delBanner/$', 'market.recommend.delBanner', name='delete banner'),
    url(r'^iplay_mgmt/market/release/$', 'market.topic.release', name='restart tomcat'),
    url(r'^iplay_mgmt/market/update/$', 'market.topic.update', name='update tomcat'),
    url(r'^iplay_mgmt/market/category/$', 'market.category.index', name='index category'),
    url(r'^iplay_mgmt/market/category_addGame/$', 'market.category.addGame', name='addGame category'),
    url(r'^iplay_mgmt/market/category_delGame/$', 'market.category.delGame', name='delGame category'),
    url(r'^iplay_mgmt/market/category_editGame/$', 'market.category.editGame', name='editGame category'),
    url(r'^iplay_mgmt/market/hotsearch/$', 'market.hotsearch.index', name='index hotsearch'),
    url(r'^iplay_mgmt/market/hotsearch_add/$', 'market.hotsearch.add', name='add hotsearch'),
    url(r'^iplay_mgmt/market/hotsearch_del/$', 'market.hotsearch.delete', name='del hotsearch'),
    url(r'^iplay_mgmt/market/hotsearch_edit/$', 'market.hotsearch.edit', name='edit hotsearch'),
    url(r'^iplay_mgmt/market/hotsearch_search/$', 'market.hotsearch.search', name='search hotsearch'),
)
