#!/usr/bin/env python
#-*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "permission_suggest_management.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
