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
from market.models import GameLabelInfo, CatGame, GameCatInfo, CatToGame

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

DIR = os.getcwd()
sys.path.append(DIR)
from utils import getTimeStamp, getDate

market_log = logging.getLogger('market')

@csrf_exempt
@login_required
def index(request):
    desc_cat_id = int(request.GET.get('desc_cat_id')) if 'desc_cat_id' in request.GET else 0
    cat_id = int(request.GET.get('cat_id')) if 'cat_id' in request.GET else 1
    cats = GameCatInfo.objects.filter(parent_id=0)
    desc_cats = GameCatInfo.objects.exclude(parent_id=0)
    game_cat_infos = GameCatInfo.objects.all()
    category_id = desc_cat_id if desc_cat_id else cat_id
    games4peo = CatGame.objects.filter(category_id=category_id).order_by('manual_num')[:10]
    games4system = CatToGame.objects.filter(category_id=category_id).order_by('order_by_dl_cnt')[:50]
    games4sys = []
    peo = set()
    for game in games4peo:
        game_id = game.game_id
        gamelabel = GameLabelInfo.objects.get(game_id=game_id)
        game.game_enabled = gamelabel.enabled
        game.game_name = gamelabel.game_name
        game.release_date = getDate(game.release_date)
        game.unrelease_date = getDate(game.unrelease_date)
        peo.add(game_id)
    for game in games4system:
        game_id = game.game_id
        gamelabel = GameLabelInfo.objects.get(game_id=game_id)
        game.enabled = gamelabel.enabled
        game.game_name = gamelabel.game_name
        if game_id not in peo: 
            games4sys.append(game)
    return render_to_response('market/category/index.html', {
            'html': '/iplay_mgmt/market/category/',
            'cats': cats,
            'desc_cats': desc_cats,
            'cat_id': cat_id,
            'desc_cat_id': desc_cat_id,
            'games4peo': games4peo,
            'games4sys': games4sys,
            'game_cat_infos': game_cat_infos 
        }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def addGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    desc_cats = request.GET.get('desc_cat_id')
    cat_id = request.GET.get('cat_id')
    DATE = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    game = {'release_date': DATE}
    return render_to_response('market/category/game_edit.html', {
            'desc_cats': desc_cats,
            'cat_id': cat_id,
            'game': game
        }, context_instance=RequestContext(request))

@login_required
def alterGame(request):
    game_id = request.GET.get('game_id')
    desc_cats = request.GET.get('desc_cat_id')
    cat_id = request.GET.get('cat_id')
    category_id = desc_cats if desc_cats else cat_id
    game = CatGame.objects.get(game_id=game_id,category_id=category_id)
    game.release_date = getDate(game.release_date)
    game.unrelease_date = getDate(game.unrelease_date)
    return render_to_response('market/category/game_edit.html', {
            'desc_cats': desc_cats,
            'cat_id': cat_id,
            'game': game
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def delGame(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    game_id = request.POST.get('game_id')
    manual_num = request.POST.get('manual_num')
    desc_cat_id = int(request.POST.get('desc_cat_id')) if 'desc_cat_id' in request.POST else 0
    cat_id = int(request.POST.get('cat_id')) if 'cat_id' in request.POST else 1
    category_id = desc_cat_id if desc_cat_id else cat_id
    CatGame.objects.get(game_id=game_id,category_id=category_id).delete()
    market_log.debug('%s%s 删除%s分类下的游戏:%s' % (user.last_name, user.first_name, str(category_id), str(game_id)))
    game_sort(category_id)
    result = '%s已被删除' % str(game_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def editGame(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    game_id = request.POST.get('game_id')
    manual_num = request.POST.get('manual_num')
    release_date = request.POST.get('release_date')
    unrelease_date = request.POST.get('unrelease_date')
    desc_cat_id = int(request.POST.get('desc_cat_id')) if 'desc_cat_id' in request.POST else 0
    cat_id = int(request.POST.get('cat_id')) if 'cat_id' in request.POST else 1
    category_id = desc_cat_id if desc_cat_id else cat_id

    release_date = getTimeStamp(release_date) if release_date else 0
    unrelease_date = getTimeStamp(unrelease_date) if unrelease_date else 0

    try:
        game = CatGame.objects.get(game_id=game_id,category_id=category_id)
        CatGame.objects.filter(game_id=game_id,category_id=category_id).update(manual_num=manual_num,release_date=release_date,unrelease_date=unrelease_date)
    except:
        game = GameLabelInfo.objects.get(game_id=game_id)
        game_name = game.game_name
        games = CatGame(game_id=game_id,category_id=category_id,game_name=game_name,manual_num=manual_num,release_date=release_date,unrelease_date=unrelease_date,enabled=0)
        games.save()
    response.write(str(game_id))
    return response

@csrf_exempt
@login_required
def isenabledGame(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    game_id = request.POST.get('game_id')
    desc_cat_id = int(request.POST.get('desc_cat_id')) if 'desc_cat_id' in request.POST else 0
    cat_id = int(request.POST.get('cat_id')) if 'cat_id' in request.POST else 1
    category_id = desc_cat_id if desc_cat_id else cat_id

    CatGame.objects.filter(game_id=game_id,category_id=category_id).update(enabled=1)

    result = '%s 已启用!!!' % str(game_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def notenabledGame(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    game_id = request.POST.get('game_id')
    desc_cat_id = int(request.POST.get('desc_cat_id')) if 'desc_cat_id' in request.POST else 0
    cat_id = int(request.POST.get('cat_id')) if 'cat_id' in request.POST else 1
    category_id = desc_cat_id if desc_cat_id else cat_id

    CatGame.objects.filter(game_id=game_id,category_id=category_id).update(enabled=0)

    result = '%s 已禁用!!!' % str(game_id)
    response.write(result)
    return response

def game_sort(category_id):
    order_num = 0
    games = CatGame.objects.filter(category_id=category_id).order_by('manual_num')
    for game in games:
        order_num += 1
        game_id = game.game_id
        CatGame.objects.filter(game_id=game_id,category_id=category_id).update(order_num=order_num)
