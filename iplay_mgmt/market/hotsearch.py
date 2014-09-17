# -*- coding:utf-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Count, Sum, connection
from django.contrib.auth.models import User
from market.models import GameLabelInfo, CatGame, GameCatInfo, CatToGame, HotSearch

import os
import re
import csv
import time
import json
import datetime
import logging
import subprocess
from urllib import quote_plus

import sys
reload(sys)
sys.setdefaultencoding('utf8')

market_log = logging.getLogger('market')

@csrf_exempt
@login_required
def index(request):
    words = HotSearch.objects.all().order_by('order_num')
    return render_to_response('market/hotsearch/index.html', {
            'html': '/iplay_mgmt/market/hotsearch/',
            'words': words
        }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def add(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    word = request.POST.get('word')
    order_num = request.POST.get('order_num')
    hotsearch = HotSearch(word=word,order_num=order_num)
    hotsearch.save()
    market_log.debug('%s%s 新增热门词:%s' % (user.last_name, user.first_name, word))
    result = '%s已增加' % str(word)
    response.write(result)
    return response


@csrf_exempt
@login_required
def delete(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    word = request.POST.get('word')
    HotSearch.objects.get(word=word).delete()
    market_log.debug('%s%s 删除热门词:%s' % (user.last_name, user.first_name, word))
    result = '%s已被删除' % str(word)
    response.write(result)
    return response


@csrf_exempt
@login_required
def edit(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    word = request.POST.get('word')
    order_num = request.POST.get('order_num')
    HotSearch.objects.filter(word=word).update(order_num=order_num)
    market_log.debug('%s%s 编辑热门词%s的序号:%s' % (user.last_name, user.first_name, word, str(order_num)))
    result = '%s已被编辑' % str(word)
    response.write(result)
    return response

@csrf_exempt
@login_required
def search(request):
    word = request.GET.get('word')
    search_shell = '/opt/lucence/bin/searchgames2.sh %s 10' % word
    search_result = json.loads(os.popen(search_shell).readlines()[0].strip())   

    games = []
    number = 1
    for game_id in search_result:
        game = GameLabelInfo.objects.get(game_id=game_id)
        game.index = number 
        games.append(game)
        number += 1
    '''
    games = []
    for game_id in search_result:
        game = GameLabelInfo.objects.get(game_id=game_id)
        games.append(game)
    '''
    return render_to_response('market/hotsearch/result.html', {
            'word': word,
            'search_result': search_result,
            'game': game,
            'games': games
        }, context_instance=RequestContext(request))
