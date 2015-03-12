#!/usr/bin/env python
#-*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


"""
WSGI config for permission project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "permission_suggest_management.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
