#!/usr/bin/env python
#-*- coding:utf-8 -*-


from django.conf.urls import patterns, include, url

from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'feedback_mgmt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^iplay_mgmt/admin/', include(admin.site.urls)),
    url(r'^', include('market.urls')),
    url(r'^', include('game.urls')),
    url(r'^', include('accounts.urls')),
)

if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^/iplay_mgmt/static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
