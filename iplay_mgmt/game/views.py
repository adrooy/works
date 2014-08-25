#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'limingdong'


from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import GameLabelInfo, GamePkgInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from json import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.db import connection

import os


class DjangoJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, QuerySet):
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)

@csrf_exempt
@login_required
def search(request):
    search_game_name = request.GET.get('search_game_name')
    games = GameLabelInfo.objects.filter(game_name__contains=search_game_name).order_by('-download_counts')[:20]
    #a= os.system('/opt/lucence/bin/searchgames2.sh 飞车 20')
    #search_game_name = request.GET.get('search_game_name')
    #a = ['01877eec', '314e8bd5', '68f580e0']
    #games = []
    #for game_id in a:
    #    game = GameLabelInfo.objects.get(game_id=game_id)
    #    games.append(game)
    feedback, page_range, per_page = lbe_pagination(request, games)
    count = len(games)
    count_page = count / 25
    # print count, page_range, per_page
    return render_to_response('game/search.html', {
        'feedback': feedback,
        'page_range': page_range,
        'per_page': per_page,
        'count': count,
        'count_page': count_page
    }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def addScreen(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    game_id = request.POST.get('game_id')
    screen_shot_url = request.POST.get('screen_shot_url')
    info = GameLabelInfo.objects.get(game_id=game_id)
    screen_shot_urls = '%s\n%s' % (info.screen_shot_urls, screen_shot_url)
    info = GameLabelInfo.objects.filter(game_id=game_id).update(screen_shot_urls=screen_shot_urls)
    result = 'yes'
    response.write(result)
    return response

@csrf_exempt
@login_required
def detail(request):

    game_id = request.GET.get('game_id')
    channels = []
    info = GameLabelInfo.objects.get(game_id=game_id)
    pkgs = GamePkgInfo.objects.filter(game_id=game_id)
    for pkg in pkgs:
        channels.append(pkg.market_channel)
    channels = list(set(channels))
    color_labels = info.color_label.strip().split('\n') if info.color_label else []
    #screen_shot_urls = info.screen_shot_urls.replace('http://ggfile.qiniudn.com/', '').strip().split('\n') if info.screen_shot_urls else []
    screen_shot_urls = []
    if info.screen_shot_urls:
        num = 1
        for screen_shot_url in info.screen_shot_urls.strip().split('\n'):
            a = {}
            a['url'] = screen_shot_url
            a['num'] = num
            num += 1
            screen_shot_urls.append(a)
    return render_to_response('game/detail.html', {
        'info': info,
        'color_labels': color_labels,
        'screen_shot_urls': screen_shot_urls,
        'channels': channels,
        'pkg': pkgs[0]
    }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def index(request):
    source = request.GET.get('source_id') if request.GET.get('source_id')  else 3
    games = GameLabelInfo.objects.filter(source=source).order_by('-download_counts')
    # print games.query
    feedback, page_range, per_page = lbe_pagination(request, games)
    count = len(games)
    count_page = count / 25
    # print count, page_range, per_page
    return render_to_response('game/show.html', {
        'feedback': feedback,
        'page_range': page_range,
        'per_page': per_page,
        'count': count,
        'count_page': count_page,
        'source': int(source)
    }, context_instance=RequestContext(request))


def label_info(request):

    error = ""
    info = ""

    if request.method == "POST" and request.is_ajax():
    # if True:
        g_id = request.POST.get('g_id')
        try:
            info = GameLabelInfo.objects.filter(game_id=g_id)
        except GamePkgInfo.DoesNotExist:
            error = "不存在"
    else:
        error = "请求错误"

    return json_return(request, error, info)


def channel(request):

    error = ""
    channels = []

    if request.method == "POST" and request.is_ajax():
    # if True:
        g_id = request.POST.get('g_id')
        # g_id = request.GET.get('id')
        # print g_id
        try:
            pkgs = GamePkgInfo.objects.filter(game_id=g_id)
            for pkg in pkgs:
                channels.append(pkg.market_channel)
            channels = list(set(channels))
        except GamePkgInfo.DoesNotExist:
            error = "不存在"
    else:
        error = "请求错误"

    return json_return(request, error, channels)


def game_info(request):

    error = ""
    # g_info = {}
    infos = ""

    if request.method == "POST" and request.is_ajax():
        g_id = request.POST.get('g_id')
        ch = request.POST.get('channel')
        try:
            if g_id and ch:
                infos = GamePkgInfo.objects.filter(
                    game_id=g_id,
                    market_channel=ch
                )

        except GamePkgInfo.DoesNotExist:
            error = "不存在"
    else:
        error = "请求错误"

    return json_return(request, error, infos)


def label_info_change(request):

    error = ""
    info = ""

    if request.method == "POST" and request.is_ajax():
        game_id = request.POST.get('game_id')
        display_name = request.POST.get('display_name')
        subscript = request.POST.get('subscript')
        color_label = request.POST.get('color_label')
        download_num = request.POST.get('download_num') or 0
        game_language = request.POST.get('language')
        star_num = request.POST.get('star') or 0
        icon_urls = request.POST.get('icon')
        screen_shot_urls = request.POST.get('screen')
        short_desc = request.POST.get('short_desc')
        detail_desc = request.POST.get('desc')
        try:
            if game_id:
                if display_name and display_name != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(display_name=display_name)
                if download_num and download_num != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(download_counts=download_num)
                if subscript and subscript != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(subscript=subscript)
                if color_label and color_label != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(color_label=color_label)
                if screen_shot_urls and screen_shot_urls != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(screen_shot_urls=screen_shot_urls)
                if icon_urls and icon_urls != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(icon_url=icon_urls)
                if short_desc and short_desc != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(short_desc=short_desc)
                if detail_desc and detail_desc != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(detail_desc=detail_desc)
                if star_num and star_num != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(star_num=star_num)
                if game_language and game_language != 'None':
                    info = GameLabelInfo.objects.filter(game_id=game_id).update(game_language=game_language)
                info = GameLabelInfo.objects.filter(game_id=game_id).update(is_changed=True)
              #  info = GameLabelInfo.objects.filter(game_id=game_id).update(
              #      display_name=display_name,
              #      download_counts=download_num,
              #      subscript=subscript,
              #      color_label=color_label,
              #      screen_shot_urls=screen_shot_urls,
              #      icon_url=icon_urls,
              #      short_desc=short_desc,
              #      detail_desc=detail_desc,
              #      star_num=star_num,
              #      game_language=game_language,
              #      is_changed=True
              #  )
                # print info
        except GameLabelInfo.DoesNotExist:
            error = "不存在"
    else:
        error = "请求错误"

    return json_return(request, error, info)


def pkg_info_change(request):

    error = ""
    info = ""

    if request.method == "POST" and request.is_ajax():
        apk_id = request.POST.get('apk_id')
        game_name = request.POST.get('game_name')
        pkg_name = request.POST.get('pkg_name')
        ver_code = request.POST.get('ver_code') or 0
        ver_name = request.POST.get('ver_name')
        size = request.POST.get('size') or 0
        download_num = request.POST.get('download_num') or 0
        game_language = request.POST.get('language')
        game_types = request.POST.get('type')
        url = request.POST.get('url')
        icon_urls = request.POST.get('icon')
        screen_shot_urls = request.POST.get('screen')
        detail_desc = request.POST.get('desc')
        try:
            if apk_id:
                info = GamePkgInfo.objects.filter(apk_id=apk_id).update(
                    game_name=game_name,
                    pkg_name=pkg_name,
                    ver_code=ver_code,
                    ver_name=ver_name,
                    file_size=size,
                    downloaded_cnts=download_num,
                    game_types=game_types,
                    screen_shot_urls=screen_shot_urls,
                    icon_urls=icon_urls,
                    game_desc=detail_desc,
                    download_url=url,
                    game_language=game_language,
                    is_change=True
                )
                # print info
        except GameLabelInfo.DoesNotExist:
            error = "不存在"
    else:
        error = "请求错误"

    return json_return(request, error, info)


def json_return(request, error, msg):
    """
    json返回，400为错误，200为成功
    :param request:
    :param error: 错误信息
    """

    if error:
        json_dict = {
            'status': 400,
            'error': error,
        }
        json = dumps(json_dict, cls=DjangoJSONEncoder)
    else:
        json_dict = {
            'status': 200,
            'success': '成功',
            'msg': msg
        }
        json = dumps(json_dict, cls=DjangoJSONEncoder)
    # print json
    return HttpResponse(json)


def lbe_pagination(request, queryset, after_range_num=5, before_range_num=4):
    """
    分页方法
    :param request:
    :param queryset:
    :param after_range_num:
    :param before_range_num:
    :return:
    """

    try:
        #得到request中的page参数
        per_page = int(request.GET.get('pr'))  # 每页记录数
    except:
        per_page = 25  # 默认为10

    per_page = 25
    #按参数分页
    paginator = Paginator(queryset, per_page)

    try:
        page_num = int(request.GET.get('pn'))  # 页码
    except:
        page_num = 1  # 默认为1

    try:
        objects = paginator.page(page_num)  # 尝试获得分页列表
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)  # 如果页数不存在，获得最后一页
    except PageNotAnInteger:
        objects = paginator.page(1)  # 如果不是一个整数，获得第一页

    #根据参数配置导航显示范围
    if page_num >= after_range_num:
        page_range = paginator.page_range[page_num - after_range_num: page_num + before_range_num]
    else:
        page_range = paginator.page_range[0: page_num + before_range_num]

    return objects, page_range, per_page


"""
SELECT pkg.id, pkg.pkg_name, pkg.version, pkg.game_basic_info_id, pkg.channel, pkg.url1, pkg.language, pkg.install_num, pkg.size, basic_many.*
FROM game_pkg_info pkg
LEFT JOIN game_basic_info_many basic_many
ON pkg.game_basic_info_id = basic_many.game_basic_info_id
AND pkg.channel = basic_many.channel
WHERE pkg.game_basic_info_id = 1
AND pkg.channel = '百度'
;
"""
