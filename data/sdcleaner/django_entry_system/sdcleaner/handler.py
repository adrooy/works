#! -*- coding:utf-8 -*-


__author__ = 'shaozuozhen'


from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Count, Sum, connection
from django.contrib.auth.models import User
from sdcleaner.models import ApkInfo, PathInfo

import os
import re
import csv
import time
import json
import datetime
import MySQLdb
import logging
import subprocess
from urllib import quote_plus
import hashlib

import sys
reload(sys)
sys.setdefaultencoding('utf8')

log = logging.getLogger('sdcleaner')

PAGE_RECORDS = 25


def _get_times(assign_to):
    assign_times = {}
    apk_list = ApkInfo.objects.filter(assign_to=assign_to)
    for i in apk_list:
        assign_times.setdefault(i.assign_time.strftime('%Y-%m-%d'))
    return assign_times

@csrf_exempt
@login_required
def page(request):

    username = request.session.get('username')
    user = User.objects.get(username=username)
    is_superuser = user.is_superuser

    finished = request.GET.get('finished') if request.GET.get('finished') else request.session.get('finished')
    approved = request.GET.get('approved') if request.GET.get('approved') else request.session.get('approved')

    request.session['finished'] = finished
    request.session['approved'] = approved

    assign_to = request.GET.get('assign_to')
    assign_time = request.GET.get('assign_time')

    if user.is_superuser:
        assign_tos = ApkInfo.objects.exclude(assign_to='').exclude(assign_to=None).values('assign_to').annotate(count=Count('assign_to'))
        if not assign_to:
            for i in assign_tos:
                assign_to = i['assign_to']
        assign_times = _get_times(assign_to)
        if not assign_time:
            for assign_time in assign_times:
                pass
        finished = finished if finished else 0 
        approved = approved if approved else 0 
        Year = str(assign_time).split('-')[0]
        Month = str(assign_time).split('-')[1]
        Day = str(assign_time).split('-')[2]
        titles = ApkInfo.objects.filter(assign_to=assign_to, approved=approved,
                finished=finished, assign_time__year=Year,
                assign_time__month=Month, assign_time__day=Day)
    else:
        if not assign_to:
            assign_to = '%s%s' % (user.last_name, user.first_name)
        finished = finished if finished else 0 
        assign_tos = ApkInfo.objects.filter(assign_to=assign_to).values('assign_to').annotate(count=Count('assign_to'))
        assign_times = _get_times(assign_to)
        if not assign_time:
            for assign_time in assign_times:
                pass
        finished = finished if finished else 0 
        approved = approved if approved else 0 
        Year = str(assign_time).split('-')[0]
        Month = str(assign_time).split('-')[1]
        Day = str(assign_time).split('-')[2]
        titles = ApkInfo.objects.filter(assign_to=assign_to, approved=approved,
                finished=finished, assign_time__year=Year,
                assign_time__month=Month, assign_time__day=Day)

    paginator = Paginator(list(titles), PAGE_RECORDS)

    after_range_num = 5
    before_range_num = 6

    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        titles = paginator.page(page)
    except PageNotAnInteger:
        titles = paginator.page(1)
    except EmptyPage:
        titles = paginator.page(1)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:
        page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]

    return render_to_response('sdcleaner/page.html', {
            'is_superuser': is_superuser,
            'titles': titles,
            'page_range': page_range,
            'user': user,
            'approved': approved,
            'finished': finished,
            'assign_to': assign_to,
            'assign_tos': assign_tos,
            'assign_time': assign_time,
            'assign_times': assign_times,
            }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def selected(request):

    username = request.session.get('username')
    user = User.objects.get(username=username)
    is_superuser = user.is_superuser
    
    assign_to = request.GET.get('assign_to')
    #version = request.GET.get('version')
    title = request.GET.get('title')
    page = request.GET.get('page')
    apk_id = request.GET.get('apk_id')
    assign_time = request.GET.get('assign_time')
    package_name = request.GET.get('package_name')

    path_infos = PathInfo.objects.filter(apk_id=apk_id)
    apk_info = ApkInfo.objects.get(id=apk_id)

    return render_to_response('sdcleaner/detail.html', {
            'is_superuser': is_superuser,
            'title': title,
            'package_name': package_name,
            'assign_to': assign_to,
            'path_infos': path_infos,
            'page': page,
            'assign_time': assign_time,
            'apk_id': apk_id,
            'comments': apk_info.comments,
            'is_finished': apk_info.finished,
            }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def save(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    apk_id = request.POST.get('apk_id')
    add_paths = json.loads(request.POST.get('add_paths'))
    update_paths = json.loads(request.POST.get('update_paths'))
    delete_paths = json.loads(request.POST.get('delete_paths'))
    comments = request.POST.get('comments')
    finished = request.POST.get('is_finished')

    #update_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    try:
        for add_path in add_paths:
            path_hash = hashlib.sha1(add_path['file_path']).hexdigest()[:10]
            PathInfo.objects.create(file_path=add_path['file_path'],item_name=add_path['item_name'],desc=add_path['desc'],alert_info=add_path['alert_info'],sub_path=add_path['sub_path'],sl=add_path['sl'],apk_id=apk_id,path_hash=path_hash)
        for update_path in update_paths:
            PathInfo.objects.filter(id=update_path['id']).update(file_path=update_path['file_path'],item_name=update_path['item_name'],desc=update_path['desc'],alert_info=update_path['alert_info'],sub_path=update_path['sub_path'],sl=update_path['sl'])
        for delete_path in delete_paths:
            PathInfo.objects.filter(id=delete_path).delete()

        ApkInfo.objects.filter(id=apk_id).update(finished=finished,comments=comments)
    except Exception as e:
        result = "保存出错，请检查数据并重试。"+str(e)
        response.write(result)
        return response

    result = '已保存!'
  
    response.write(result)
    return response

@csrf_exempt
@login_required
def approve(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    apk_id = request.POST.get('apk_id')
    ApkInfo.objects.filter(id=apk_id).update(approved=1)
    
    result = '设为已通过，完成!'
    response.write(result)
    return response

@csrf_exempt
@login_required
def disapprove(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    apk_id = request.POST.get('apk_id')
    ApkInfo.objects.filter(id=apk_id).update(approved=0)

    result = '设为未通过, 完成!'
    response.write(result)
    return response

@csrf_exempt
@login_required
def pend(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    apk_id = request.POST.get('apk_id')
    ApkInfo.objects.filter(id=apk_id).update(approved=2)

    result = '设为待定,完成!'
    response.write(result)
    return response

@csrf_exempt
@login_required
def download(request):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
 
    #assign_to = request.GET.get('assign_to')
    #category = request.GET.get('category')
    apk_id = request.GET.get('apk_id')
    apk_info = ApkInfo.objects.get(id=apk_id)
   
    package_name = apk_info.package_name
    title = apk_info.title
    version_code = apk_info.version_code

    #try:
    if 1==1:
    	fileName = '%s_&_%s_&_%s.apk' % (str(title), str(package_name), str(version_code))
    	f = open(os.path.join(BASE_DIR, 'apkfolder/%s' % fileName))
    	response = HttpResponse(FileWrapper(f), content_type='text/plain')
    	response['Content-Disposition'] = 'attachment; filename=%s' % (fileName).replace(' ', '_').replace(':', '_')
    	return response
    #except:
	fileName = '%s_%s_%s.apk' % (str(title), str(package_name), str(version_code))
    	f = open(os.path.join(BASE_DIR, 'apkfolder/old/%s/%s' % (category.encode('utf8'), fileName)))
     	response = HttpResponse(FileWrapper(f), content_type='text/plain')
    	response['Content-Disposition'] = 'attachment; filename=%s' % (fileName).replace(' ', '_')
    	return response
