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

DIR = os.getcwd()
sys.path.append(DIR)
from utils import getTimeStamp, getDate

market_log = logging.getLogger('market')


@csrf_exempt
@login_required
def release(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    os.system('python /root/operation/step_09_gen_mapping_tables_for_service/09_8_gen_category_to_game_result.py')
    os.system("wget -O - 'http://127.0.0.1:8080/gamecommunity/instruction!clear.action?name=table'")
    result = '发布完成'
    market_log.debug('%s%s 发布数据' % (user.last_name, user.first_name))
    response.write(result)
    return response

@csrf_exempt
@login_required
def update(request):
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)
    os.system("sh /root/operation/cmd/cmd_sync_small_crack.sh")
    result = '同步完成'
    market_log.debug('%s%s 同步数据' % (user.last_name, user.first_name))
    response.write(result)
    return response

@csrf_exempt
@login_required
def check(request):
    os.system("python /opt/www/iplay_mgmt/shell/check_data.py > /opt/www/iplay_mgmt/shell/log")
    return render_to_response('market/check.html', {
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def index(request):
    topic_id = int(request.GET.get('topic_id')) if 'topic_id' in request.GET else 0
 
    topics = TopicInfo.objects.all().order_by('order_num')
    for topic in topics:
        topic.topic_date = getDate(topic.topic_date)
        topic.unrelease_date = getDate(topic.unrelease_date)
    return render_to_response('market/topic/index.html', {
            'html': '/iplay_mgmt/market/topic/',
            'topic_id': topic_id,
            'topics': topics
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def add(request):
    topic_id_index = request.GET.get('topic_id')
    if topic_id_index == 'undefined':
        topic_id_index = ''
    DATE = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    topic = {'topic_date': DATE}
    return render_to_response('market/topic/edit.html', {
            'topic': topic,
            'topic_id_index': topic_id_index
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def alter(request):
    topic_id = request.GET.get('topic_id')
    gameid = request.GET.get('game_id')
    
    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
    topic = TopicInfo.objects.get(id=topic_id)
    topic.topic_date = getDate(topic.topic_date)
    topic.unrelease_date = getDate(topic.unrelease_date)
 
    for game in games:
        game_id = game.game_id
        gamelabel = GameLabelInfo.objects.get(game_id=game_id)
        game.enabled = gamelabel.enabled
    return render_to_response('market/topic/edit.html', {
            'games': games,
            'topic': topic,
            'game_id': gameid,
            'topic_id':topic_id
        }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def edit(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)

    topic_id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    short_desc = request.POST.get('short_desc', '')
    detail_desc = request.POST.get('detail_desc', '')
    pic_url = request.POST.get('pic_url', '')
    topic_id_index = request.POST.get('topic_id_index', '')
    topic_date = request.POST.get('topic_date')
    unrelease_date = request.POST.get('unrelease_date')

    if not name or not short_desc or not pic_url:
        response.write('请输入专题信息!!!')
        return response

    topic_date = getTimeStamp(topic_date) if topic_date else 0
    unrelease_date = getTimeStamp(unrelease_date) if unrelease_date else 0

    if topic_id:
        "专题存在　更新信息"
        TopicInfo.objects.filter(id=topic_id).update(name=name,
                short_desc=short_desc, detail_desc=detail_desc,
                pic_url=pic_url, topic_date=topic_date, unrelease_date=unrelease_date)
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
                topic_date=topic_date, order_num=order_num_index, enabled=0, unrelease_date=unrelease_date)
        topic.save()

        topics = TopicInfo.objects.all().order_by('id')
        for topic in topics:
            topic_id = topic.id
        result = '%s专题已添加!!!' % str(topic_id)
        market_log.debug('%s%s 新增专题:%s' % (user.last_name, user.first_name, str(topic_id)))
    else:
        order_num = 1
        topics = TopicInfo.objects.all().order_by('order_num')
        for topic in topics:
            topic_id = topic.id
            order_num += 1
            TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)

        topic = TopicInfo(name=name, short_desc=short_desc,
                detail_desc=detail_desc, pic_url=pic_url,
                topic_date=topic_date, order_num=1, enabled=0, unrelease_date=unrelease_date)
        topic.save()

        topics = TopicInfo.objects.all().order_by('id')
        for topic in topics:
            topic_id = topic.id
        market_log.debug('%s%s 新增专题:%s' % (user.last_name, user.first_name, str(topic_id)))
    response.write(topic_id)
    return response

@csrf_exempt
@login_required
def isenabled(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)

    id = request.POST.get('topic_id')

    TopicInfo.objects.filter(id=id).update(enabled=1)
    market_log.debug('%s%s 启用专题:%s' % (user.last_name, user.first_name, str(id)))

    result = '%s 已启用!!!' % str(id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def notenabled(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'
    username = request.session.get('username')
    user = User.objects.get(username=username)

    id = request.POST.get('topic_id')

    TopicInfo.objects.filter(id=id).update(enabled=0)
    market_log.debug('%s%s 禁用专题:%s' % (user.last_name, user.first_name, str(id)))

    result = '%s 已禁用!!!' % str(id)
    response.write(result)
    return response

@csrf_exempt
@login_required
def move(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    topic_id = request.POST.get('topic_id')
    index = int(request.POST.get('index'))
    old_index = int(TopicInfo.objects.get(id=topic_id).order_num)

    topics = TopicInfo.objects.all().order_by('order_num')
    indexs = []
    new_indexs = []
    for topic in topics:
        indexs.append(topic.id)
    if index <= 1:
        index = 1
    if index >= len(indexs):
        index = len(indexs)
    
    if old_index > index:
        new_indexs = indexs[:index-1] + [topic_id] + indexs[index-1:old_index-1] + indexs[old_index:]
        order_num = 1
        for topic_id in new_indexs:
            TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)
            order_num += 1
    elif old_index < index:
        new_indexs = indexs[:old_index-1] + indexs[old_index:index] + [topic_id] + indexs[index:]
        order_num = 1
        for topic_id in new_indexs:
            TopicInfo.objects.filter(id=topic_id).update(order_num=order_num)
            order_num += 1
    else:
        pass

    result = str(indexs) + '\n' + str(new_indexs)
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
    username = request.session.get('username')
    user = User.objects.get(username=username)

    topic_id = request.POST.get('topic_id')

    TopicInfo.objects.get(id=topic_id).delete()
    market_log.debug('%s%s 删除专题:%s' % (user.last_name, user.first_name, str(topic_id)))

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
    username = request.session.get('username')
    user = User.objects.get(username=username)

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
            market_log.debug('%s%s 新增专题%s的游戏列表:%s' % (user.last_name, user.first_name, str(topic_id), game_id))
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
            market_log.debug('%s%s 新增专题%s的游戏列表:%s' % (user.last_name, user.first_name, str(topic_id), game_id))
            result = '%s已添加到%s!!!' % (game_name, str(topic_id))
   
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
    topic_id = request.POST.get('topic_id')

    TopicGame.objects.get(game_id=game_id, topic_id=topic_id).delete()
    market_log.debug('%s%s 删除专题%s的游戏列表:%s' % (user.last_name, user.first_name, str(topic_id), game_id))
 
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
def moveGame(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')
    topic_id = request.POST.get('topic_id')
    index = int(request.POST.get('index'))
    old_index = int(TopicGame.objects.get(game_id=game_id,topic_id=topic_id).order_num)

    games = TopicGame.objects.filter(topic_id=topic_id).order_by('order_num')
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
            TopicGame.objects.filter(topic_id=topic_id,game_id=game_id).update(order_num=order_num)
            order_num += 1
    elif old_index < index:
        new_indexs = indexs[:old_index-1] + indexs[old_index:index] + [game_id] + indexs[index:]
        order_num = 1
        for game_id in new_indexs:
            TopicGame.objects.filter(topic_id=topic_id,game_id=game_id).update(order_num=order_num)
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
