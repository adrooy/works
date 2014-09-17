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
from market.models import RecBanner, RecGame, GameLabelInfo, TopicInfo

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
    gameid = request.GET.get('game_id')
    bannerid = int(request.GET.get('banner_id')) if 'banner_id' in request.GET else 0
    games = RecGame.objects.all().order_by('order_num')
    banners = RecBanner.objects.all().order_by('order_num')
    for banner in banners:
        banner.release_date = getDate(banner.release_date)
        banner.unrelease_date = getDate(banner.unrelease_date)
    for game in games:
            game_id = game.game_id
            gamelabel = GameLabelInfo.objects.get(game_id=game_id)
            game.game_enabled = gamelabel.enabled
            game.release_date = getDate(game.release_date)
            game.unrelease_date = getDate(game.unrelease_date)
    return render_to_response('market/recommend/index.html', {
            'html': '/iplay_mgmt/market/recommend/',
            'game_id': gameid,
            'banner_id': bannerid,
            'games': games,
            'banners': banners
            }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def addGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    game_id_index = request.GET.get('game_id')
    if game_id_index == 'undefined':
        game_id_index = ''

    DATE = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    game = {'release_date': DATE}
 
    return render_to_response('market/recommend/game_edit.html', {
            'game': game,
            'game_id_index': game_id_index
        }, context_instance=RequestContext(request))

@login_required
def altGame(request):
    game_id = request.GET.get('game_id')
    game = RecGame.objects.get(game_id=game_id)
    game.release_date = getDate(game.release_date)
    game.unrelease_date = getDate(game.unrelease_date)
    return render_to_response('market/recommend/game_edit.html', {
            'game': game,
            'game_id':game_id
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def editGame(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    game_id = request.POST.get('game_id')
    manual_num = request.POST.get('manual_num')
    game_id_index = request.POST.get('game_id_index')
    release_date = request.POST.get('release_date')
    unrelease_date = request.POST.get('unrelease_date')

    release_date = getTimeStamp(release_date) if release_date else 0
    unrelease_date = getTimeStamp(unrelease_date) if unrelease_date else 0

    try:
        game = RecGame.objects.get(game_id=game_id)
        game_name = game.game_name
        RecGame.objects.filter(game_id=game_id).update(manual_num=manual_num,release_date=release_date,unrelease_date=unrelease_date)
    except:
        game = GameLabelInfo.objects.get(game_id=game_id)
        game_name = game.game_name
        games = RecGame(game_id=game_id,game_name=game_name,manual_num=manual_num,release_date=release_date,unrelease_date=unrelease_date,enabled=0)
        games.save()
    response.write(str(game_id))
    return response

@csrf_exempt
@login_required
def isenabledGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')

    RecGame.objects.filter(game_id=game_id).update(enabled=1)

    result = '%s 已启用!!!' % str(game_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def notenabledGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')

    RecGame.objects.filter(game_id=game_id).update(enabled=0)

    result = '%s 已禁用!!!' % str(game_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def delGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    game_id = request.POST.get('game_id')
    RecGame.objects.get(game_id=game_id).delete()
    market_log.debug('%s%s 删除推荐列表的游戏:%s' % (user.last_name, user.first_name, str(game_id)))

    order_num = 1
    games = RecGame.objects.all().order_by('order_num')
    for game in games:
        game_id = game.game_id
        RecGame.objects.filter(game_id=game_id).update(order_num=order_num)
        order_num += 1
    
    result = '推荐游戏列表页的%s游戏已删除！！！' % str(len(games))
    response.write(result)
    return response

@csrf_exempt
@login_required
def moveGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')
    index = int(request.POST.get('index'))
    old_index = int(RecGame.objects.get(game_id=game_id).order_num)

    games = RecGame.objects.all().order_by('order_num')
    indexs = []
    new_indexs = []
    for game in games:
        indexs.append(game.game_id)
    if index <= 1:
        index = 1
    if index >= len(indexs):
        index = len(indexs)
    

    if old_index > index:
        new_indexs = indexs[:index-1] + [game_id] + indexs[index-1:old_index-1] + indexs[old_index:]
        order_num = 1
        for game_id in new_indexs:
            RecGame.objects.filter(game_id=game_id).update(order_num=order_num)
            order_num += 1
    elif old_index < index:
        new_indexs = indexs[:old_index-1] + indexs[old_index:index] + [game_id] + indexs[index:]
        order_num = 1
        for game_id in new_indexs:
            RecGame.objects.filter(game_id=game_id).update(order_num=order_num)
            order_num += 1
    else:
        pass

    result = str(indexs) + '\n' + str(new_indexs)
    response.write(result)
    return response

@csrf_exempt
@login_required
def upGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')

    indexs = []
    games = RecGame.objects.all().order_by('order_num')
 
    for game in games:
        indexs.append(game.game_id) 
        if game.game_id == game_id:
            game_name = game.game_name

    up_num = indexs.index(game_id)
    num = up_num + 1
    up_id = indexs[up_num-1]

    if up_num:
        num = up_num + 1
        up_id = indexs[up_num-1]
        RecGame.objects.filter(game_id=game_id).update(order_num=up_num)
        RecGame.objects.filter(game_id=up_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response

@csrf_exempt
@login_required
def downGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')

    indexs = []
    games = RecGame.objects.all().order_by('order_num')
 
    for game in games:
        indexs.append(game.game_id) 
        if game.game_id == game_id:
            game_name = game.game_name

    up_num = indexs.index(game_id)
    num = up_num + 1
    down_num = num + 1
    if down_num < len(games)+1:
        num = up_num + 1
        down_num = num + 1
        down_id = indexs[up_num+1]
        RecGame.objects.filter(game_id=game_id).update(order_num=down_num)
        RecGame.objects.filter(game_id=down_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response

@csrf_exempt
@login_required
def addBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    banner_id_index = request.GET.get('banner_id')
    if banner_id_index == 'undefined':
        banner_id_index = ''

    DATE = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    banner = {'release_date': DATE}
 
    return render_to_response('market/recommend/edit.html', {
            'banner': banner,
            'banner_id_index': banner_id_index
        }, context_instance=RequestContext(request))

@login_required
def alterBanner(request):
    banner_id = request.GET.get('banner_id')
    banner = RecBanner.objects.get(id=banner_id) if banner_id else {}
    banner.release_date = getDate(banner.release_date)
    banner.unrelease_date = getDate(banner.unrelease_date)
    return render_to_response('market/recommend/edit.html', {
            'banner': banner,
            'banner_id':banner_id
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def editBanner(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    banner_id = request.POST.get('banner_id')
    name = request.POST.get('name')
    game_id = request.POST.get('game_id')
    topic_id = request.POST.get('topic_id')
    pic_url = request.POST.get('pic_url')
    banner_id_index = request.POST.get('banner_id_index')
    release_date = request.POST.get('release_date')
    unrelease_date = request.POST.get('unrelease_date')

    release_date = getTimeStamp(release_date) if release_date else 0
    unrelease_date = getTimeStamp(unrelease_date) if unrelease_date else 0

    if banner_id:
        if str(topic_id) != 'None':
            RecBanner.objects.filter(id=banner_id).update(name=name,topic_id=topic_id,pic_url=pic_url,release_date=release_date,unrelease_date=unrelease_date)
        else:
            RecBanner.objects.filter(id=banner_id).update(name=name,game_id=game_id,pic_url=pic_url,release_date=release_date,unrelease_date=unrelease_date)
        result = '更新'
    elif banner_id_index:
            order_num = 1
            banner = RecBanner.objects.get(id=banner_id_index)
            order_num_index = banner.order_num

            banners = RecBanner.objects.all().order_by('order_num')
            for banner in banners:
                banner_id = banner.id
                if int(banner_id) == int(banner_id_index):
                    order_num += 1
                RecBanner.objects.filter(id=banner_id).update(order_num=order_num)
                order_num += 1
            try:
                game = GameLabelInfo.objects.get(game_id=game_id)
                if not name:
                    name = game.game_name
                banner = RecBanner(game_id=game_id,name=name,order_num=order_num_index,pic_url=pic_url,enabled=0,release_date=release_date,unrelease_date=unrelease_date)
                banner.save()
                result = '%s %s %s 更新' % (str(banner_id_index), str([banner_id]), str(topic_id))
                market_log.debug('%s%s 新增banner:%s' % (user.last_name, user.first_name, str(game_id)))
            except:
                try:
                    topic = TopicInfo.objects.get(id=topic_id)
                    if not name:
                        name = topic.name
                    banner = RecBanner(topic_id=topic_id,name=name,order_num=order_num_index,pic_url=pic_url,enabled=0,release_date=release_date,unrelease_date=unrelease_date)
                    banner.save()
                    result = banner.id
                    result = '%s %s %s 更新' % (str(banner_id_index), str([banner_id]), str(topic_id))
                    market_log.debug('%s%s 新增banner:%s' % (user.last_name, user.first_name, str(topic_id)))
                except:
                    result = 'No'
    else:
            order_num = 1
            banners = RecBanner.objects.all().order_by('order_num')
            for banner in banners:
                order_num += 1
                banner_id = banner.id
                RecBanner.objects.filter(id=banner_id).update(order_num=order_num)
            try:
                game = GameLabelInfo.objects.get(game_id=game_id)
                if not name:
                    name = game.game_name
                banner = RecBanner(game_id=game_id,name=name,order_num=1,pic_url=pic_url,enabled=0,release_date=release_date,unrelease_date=unrelease_date)
                banner.save()
                result = banner.id
                result = '%s %s %s 更新' % (str(banner_id_index), str([banner_id]), str(topic_id))
                market_log.debug('%s%s 新增banner:%s' % (user.last_name, user.first_name, str(game_id)))
            except:
                try:
                    topic = TopicInfo.objects.get(id=topic_id)
                    if not name:
                        name = topic.name
                    banner = RecBanner(topic_id=topic_id,name=name,order_num=1,pic_url=pic_url,enabled=0,release_date=release_date,unrelease_date=unrelease_date)
                    banner.save()
                    result = '%s %s %s 更新' % (str(name), str([banner_id]), str(topic_id))
                    market_log.debug('%s%s 新增banner:%s' % (user.last_name, user.first_name, str(topic_id)))
                except:
                    result = 'No'
    response.write(result)
    return response

@csrf_exempt
@login_required
def moveBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    banner_id = request.POST.get('banner_id')
    index = int(request.POST.get('index'))
    old_index = int(RecBanner.objects.get(id=banner_id).order_num)

    banners = RecBanner.objects.all().order_by('order_num')
    indexs = []
    new_indexs = []
    for banner in banners:
        indexs.append(banner.id)
    if index <= 1:
        index = 1
    if index >= len(indexs):
        index = len(indexs)
    

    if old_index > index:
        new_indexs = indexs[:index-1] + [banner_id] + indexs[index-1:old_index-1] + indexs[old_index:]
        order_num = 1
        for banner_id in new_indexs:
            RecBanner.objects.filter(id=banner_id).update(order_num=order_num)
            order_num += 1
    elif old_index < index:
        new_indexs = indexs[:old_index-1] + indexs[old_index:index] + [banner_id] + indexs[index:]
        order_num = 1
        for banner_id in new_indexs:
            RecBanner.objects.filter(id=banner_id).update(order_num=order_num)
            order_num += 1
    else:
        pass

    result = str(indexs) + '\n' + str(new_indexs)
    response.write(result)
    return response

@csrf_exempt
@login_required
def upBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    banner_id = request.POST.get('banner_id')

    indexs = []
    banners = RecBanner.objects.all().order_by('order_num')
 
    for banner in banners:
        indexs.append(int(banner.id))
        if int(banner.id) == int(banner_id):
            name = banner.name

    up_num = indexs.index(int(banner_id))
    num = up_num + 1
    up_id = indexs[up_num-1]

    if up_num:
        num = up_num + 1
        up_id = indexs[up_num-1]
        RecBanner.objects.filter(id=banner_id).update(order_num=up_num)
        RecBanner.objects.filter(id=up_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response

@csrf_exempt
@login_required
def downBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    banner_id = request.POST.get('banner_id')

    indexs = []
    banners = RecBanner.objects.all().order_by('order_num')
 
    for banner in banners:
        indexs.append(int(banner.id)) 
        if int(banner.id) == int(banner_id):
            banner_name = banner.name

    up_num = indexs.index(int(banner_id))
    num = up_num + 1
    down_num = num + 1
    if down_num < len(banners)+1:
        num = up_num + 1
        down_num = num + 1
        down_id = indexs[up_num+1]
        RecBanner.objects.filter(id=banner_id).update(order_num=down_num)
        RecBanner.objects.filter(id=down_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response

@csrf_exempt
@login_required
def delBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
 
    banner_id = request.POST.get('banner_id')
    RecBanner.objects.get(id=banner_id).delete()
    market_log.debug('%s%s 删除banner:%s' % (user.last_name, user.first_name, str(banner_id)))

    order_num = 1
    banners = RecBanner.objects.all().order_by('order_num')
    for banner in banners:
        banner_id = banner.id
        RecBanner.objects.filter(id=banner_id).update(order_num=order_num)
        order_num += 1
    
    result = '推荐游戏列表页的%s banner已删除！！！' % str(banner_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def isenabledBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    banner_id = request.POST.get('banner_id')

    RecBanner.objects.filter(id=banner_id).update(enabled=1)

    result = '%s 已启用!!!' % str(banner_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def notenabledBanner(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    banner_id = request.POST.get('banner_id')

    RecBanner.objects.filter(id=banner_id).update(enabled=0)

    result = '%s 已禁用!!!' % str(banner_id)
    response.write(result)
    return response
