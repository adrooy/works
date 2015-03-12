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
from market.models import TopicInfo, TopicGame, GameLabelInfo

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


DATE = str(datetime.datetime.now().strftime('%Y-%m-%d'))
TIME = float(time.time())


@csrf_exempt
@login_required
def index(request):
    topics = TopicInfo.objects.all().order_by('order_num')
    return render_to_response('market/topic/index.html', {
            'topics': topics
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def add(request):
    topic_id_index = request.GET.get('topic_id')
    if topic_id_index == 'undefined':
        topic_id_index = ''
    return render_to_response('market/topic/edit.html', {
            'topic_id_index': topic_id_index
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def alter(request):
    topic_id = request.GET.get('topic_id')
    
    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
    topic = TopicInfo.objects.get(id=topic_id) if topic_id else {}
    return render_to_response('market/topic/edit.html', {
            'games': games,
            'topic': topic,
            'topic_id':topic_id
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def edit(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    short_desc = request.POST.get('short_desc', '')
    detail_desc = request.POST.get('detail_desc', '')
    pic_url = request.POST.get('pic_url', '')
    topic_id_index = request.POST.get('topic_id_index', '')

    if not name or not short_desc or not pic_url:
        response.write('请输入专题信息!!!')
        return response

    topic_date = TIME

    if topic_id:
        "专题存在　更新信息"
        TopicInfo.objects.filter(id=topic_id).update(name=name,
                short_desc=short_desc, detail_desc=detail_desc,
                pic_url=pic_url)
    elif topic_id_index:
        order_num = 1
        topic = TopicInfo.objects.get(id=topic_id_index)
        order_num_index = topic.order_num

        topics = TopicInfo.objects.all().order_by('order_num')
        for topic in topics:
            topic_id = topic.id
            if int(topic_id) == int(topic_id_index):
                order_num += 1
            TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)
            order_num += 1

        topic = TopicInfo(name=name, short_desc=short_desc,
                detail_desc=detail_desc, pic_url=pic_url,
                topic_date=topic_date, order_num=order_num_index, enabled=1)
        topic.save()

        topics = TopicInfo.objects.all().order_by('id')
        for topic in topics:
            new = topic.id
        result = '%s专题已添加!!!' % str(new)
    else:
        order_num = 1
        topics = TopicInfo.objects.all().order_by('order_num')
        for topic in topics:
            topic_id = topic.id
            order_num += 1
            TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)

        topic = TopicInfo(name=name, short_desc=short_desc,
                detail_desc=detail_desc, pic_url=pic_url,
                topic_date=topic_date, order_num=1, enabled=1)
        topic.save()

        topics = TopicInfo.objects.all().order_by('id')
        for topic in topics:
            new = topic.id
        result = '%s专题已添加!!!' % str(new)

    response.write(new)
    return response

@csrf_exempt
@login_required
def isenabled(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    id = request.POST.get('topic_id')

    TopicInfo.objects.filter(id=id).update(enabled=1)

    result = '%s 已启用!!!' % str(id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def notenabled(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    id = request.POST.get('topic_id')

    TopicInfo.objects.filter(id=id).update(enabled=0)

    result = '%s 已禁用!!!' % str(id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def up(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('topic_id')

    indexs = []
    topics = TopicInfo.objects.all().order_by('order_num')
 
    for topic in topics:
        indexs.append(int(topic.id)) 
        if int(topic.id) == int(topic_id):
            name = topic.name

    up_num = indexs.index(int(topic_id))
    num = up_num + 1
    up_id = indexs[up_num-1]

    if up_num:
        num = up_num + 1
        up_id = indexs[up_num-1]
        TopicInfo.objects.filter(id=topic_id).update(order_num=up_num)
        TopicInfo.objects.filter(id=up_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response

@csrf_exempt
@login_required
def delete(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('topic_id')

    TopicInfo.objects.get(id=topic_id).delete()

    order_num = 1
    topics = TopicInfo.objects.all().order_by('order_num')
    for topic in topics:
        topic_id = topic.id
        TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)
        order_num += 1
    
    result = '专题%s已删除！！！' % str(topic_id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def down(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('topic_id')

    indexs = []
    topics = TopicInfo.objects.all().order_by('order_num')
 
    for topic in topics:
        indexs.append(int(topic.id)) 
        if int(topic.id) == int(topic_id):
            name = topic.name

    up_num = indexs.index(int(topic_id))
    num = up_num + 1
    down_num = num + 1
    if down_num < len(topics)+1:
        num = up_num + 1
        down_num = num + 1
        down_id = indexs[up_num+1]
        TopicInfo.objects.filter(id=topic_id).update(order_num=down_num)
        TopicInfo.objects.filter(id=down_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'
    
    response.write(result)
    return response

@csrf_exempt
@login_required
def addGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    new_game_id = request.POST.get('game_id')
    game_id_index = request.POST.get('game_id_index')
    topic_id = request.POST.get('topic_id')

    try:
        game = TopicGame.objects.get(topic_id=topic_id,game_id=new_game_id)
        game_name = game.game_name
        result = '%s 已在专题列表内！！' % game_name
    except:
        if game_id_index:
            order_num = 1
            game = TopicGame.objects.get(topic_id=topic_id,game_id=game_id_index)
            order_num_index = game.order_num

            games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
            for game in games:
                game_id = game.game_id
                if game_id == game_id_index:
                    order_num += 1
                TopicGame.objects.filter(topic_id=topic_id,game_id=game_id).update(order_num=order_num)
                order_num += 1

            game_id = request.POST.get('game_id')
            game = GameLabelInfo.objects.get(game_id=game_id)
            game_name = game.game_name
            games = TopicGame(game_id=game_id,topic_id=topic_id,game_name=game_name,order_num=order_num_index)
            games.save()
            result = '%s已添加到%s!!! %s' % (game_name, str(topic_id), str(order_num_index))
        else:
            order_num = 1
            games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
            for game in games:
                order_num += 1
                game_id = game.game_id
                TopicGame.objects.filter(topic_id=topic_id,game_id=game_id).update(order_num=order_num)
                

            game_id = request.POST.get('game_id')
            game = GameLabelInfo.objects.get(game_id=game_id)
            game_name = game.game_name
            games = TopicGame(game_id=game_id,topic_id=topic_id,game_name=game_name,order_num=1)
            games.save()
            result = '%s已添加到%s!!!' % (game_name, str(topic_id))
   
    response.write(result)
    return response

@csrf_exempt
@login_required
def delGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')
    topic_id = request.POST.get('topic_id')

    TopicGame.objects.get(game_id=game_id, topic_id=topic_id).delete()

    order_num = 1
    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
    for game in games:
        game_id = game.game_id
        TopicGame.objects.filter(game_id=game_id,topic_id=topic_id).update(order_num=order_num)
        order_num += 1
    
    result = '%s下的%s游戏已删除！！！' % (str(topic_id), str(game_id))
    response.write(result)
    return response

@csrf_exempt
@login_required
def upGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('topic_id')
    game_id = request.POST.get('game_id')

    indexs = []
    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
 
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
        TopicGame.objects.filter(game_id=game_id,topic_id=topic_id).update(order_num=up_num)
        TopicGame.objects.filter(game_id=up_id,topic_id=topic_id).update(order_num=num)
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

    topic_id = request.POST.get('topic_id')
    game_id = request.POST.get('game_id')

    indexs = []
    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
 
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
        TopicGame.objects.filter(game_id=game_id,topic_id=topic_id).update(order_num=down_num)
        TopicGame.objects.filter(game_id=down_id,topic_id=topic_id).update(order_num=num)
        result = 'Yes'
    else:
        result = 'Error'

    response.write(result)
    return response
