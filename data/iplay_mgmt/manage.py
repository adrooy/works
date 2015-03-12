#!/usr/bin/python
#-*- coding:utf-8 -*-


import os
import sys

# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iplay_management.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
