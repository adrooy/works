#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: extras.py
Author: limingdong
Date: 7/25/14
Description: 
"""

from django.template import Library

register = Library()


@register.simple_tag()
def multiply(pn, sub):
    page_size = 25
    pn = pn - sub
    if pn < 1:
        pn = 0
    return pn * page_size