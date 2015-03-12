#! -*- coding:utf-8 -*-


__author__ = 'xiangxiaowei'


from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Count, Sum, connection
from django.contrib.auth.models import User
from permission.models import Suggest
from oneapp import checkVersion

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

import sys
reload(sys)
sys.setdefaultencoding('utf8')

log = logging.getLogger('checkVersion')

PAGE_RECORDS = 25


def _get_times(assign_to):
    assign_times = {}
    suggest_list = Suggest.objects.filter(assign_to=assign_to)
    for i in suggest_list:
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
        assign_tos = Suggest.objects.exclude(assign_to='').exclude(assign_to=None).values('assign_to').annotate(count=Count('assign_to'))
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
        titles = Suggest.objects.filter(assign_to=assign_to, approved=approved,
                finished=finished, assign_time__year=Year,
                assign_time__month=Month, assign_time__day=Day)
    else:
        if not assign_to:
            assign_to = '%s%s' % (user.last_name, user.first_name)
        finished = finished if finished else 0 
        assign_tos = Suggest.objects.filter(assign_to=assign_to).values('assign_to').annotate(count=Count('assign_to'))
        assign_times = _get_times(assign_to)
        if not assign_time:
            for assign_time in assign_times:
                pass
        finished = finished if finished else 0 
        approved = approved if approved else 0 
        Year = str(assign_time).split('-')[0]
        Month = str(assign_time).split('-')[1]
        Day = str(assign_time).split('-')[2]
        titles = Suggest.objects.filter(assign_to=assign_to, approved=approved,
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

    return render_to_response('permission/page.html', {
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
    version = request.GET.get('version')
    title = request.GET.get('title')
    page = request.GET.get('page')
    assign_time = request.GET.get('assign_time')
    package_name = request.GET.get('package_name')

    perms = Suggest.objects.get(assign_to=assign_to, version_code=version, package_name=package_name)

    return render_to_response('permission/suggest.html', {
            'is_superuser': is_superuser,
            'title': title,
            'assign_to': assign_to,
            'version': version,
            'perms': perms,
            'page': page,
            'assign_time': assign_time,
            }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def is_finished(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    assign_to = request.POST.get('assign_to')
 #   category = request.POST.get('category')
    title = request.POST.get('title')
    version = request.POST.get('version')
    package_name = request.POST.get('package_name')

    finished = request.POST.get('is_finished')
    finished = True if finished == '1' else False

    #update_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    perm_sendsms_suggest = request.POST.get("perm_sendsms_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_sendsms_suggest)
    perm_sendsms_description = request.POST.get("perm_sendsms_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_sendsms_description)
    perm_callphone_suggest = request.POST.get("perm_callphone_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callphone_suggest)
    perm_callphone_description = request.POST.get("perm_callphone_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callphone_description)
    perm_smsdb_suggest = request.POST.get("perm_smsdb_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_smsdb_suggest)
    perm_smsdb_description = request.POST.get("perm_smsdb_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_smsdb_description)
    perm_contact_suggest = request.POST.get("perm_contact_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_contact_suggest)
    perm_contact_description = request.POST.get("perm_contact_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_contact_description)
    perm_calllog_suggest = request.POST.get("perm_calllog_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_calllog_suggest)
    perm_calllog_description = request.POST.get("perm_calllog_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_calllog_description)
    perm_location_suggest = request.POST.get("perm_location_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_location_suggest)
    perm_location_description = request.POST.get("perm_location_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_location_description)
    perm_phoneinfo_suggest = request.POST.get("perm_phoneinfo_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_phoneinfo_suggest)
    perm_phoneinfo_description = request.POST.get("perm_phoneinfo_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_phoneinfo_description)
    perm_netdefault_suggest = request.POST.get("perm_netdefault_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_netdefault_suggest)
    perm_netdefault_description = request.POST.get("perm_netdefault_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_netdefault_description)
    perm_netwifi_suggest = request.POST.get("perm_netwifi_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_netwifi_suggest)
    perm_netwifi_description = request.POST.get("perm_netwifi_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_netwifi_description)
    perm_root_suggest = request.POST.get("perm_root_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_root_suggest)
    perm_root_description = request.POST.get("perm_root_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_root_description)
    perm_callstate_suggest = request.POST.get("perm_callstate_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callstate_suggest)
    perm_callstate_description = request.POST.get("perm_callstate_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callstate_description)
    perm_callmonitor_suggest = request.POST.get("perm_callmonitor_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callmonitor_suggest)
    perm_callmonitor_description = request.POST.get("perm_callmonitor_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_callmonitor_description)
    perm_recorder_suggest = request.POST.get("perm_recorder_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_recorder_suggest)
    perm_recorder_description = request.POST.get("perm_recorder_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_recorder_description)
    perm_settings_suggest = request.POST.get("perm_settings_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_settings_suggest)
    perm_settings_description = request.POST.get("perm_settings_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_settings_description)
    perm_autostart_suggest = request.POST.get("perm_autostart_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_autostart_suggest)
    perm_autostart_description = request.POST.get("perm_autostart_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_autostart_description)
    perm_notification_suggest = request.POST.get("perm_notification_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_notification_suggest)
    perm_notification_description = request.POST.get("perm_notification_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_notification_description)
    perm_installpackage_suggest = request.POST.get("perm_installpackage_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_installpackage_suggest)
    perm_installpackage_description = request.POST.get("perm_installpackage_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_installpackage_description)
    perm_audiorecorder_suggest = request.POST.get("perm_audiorecorder_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_audiorecorder_suggest)
    perm_audiorecorder_description = request.POST.get("perm_audiorecorder_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_audiorecorder_description)
    perm_mmsdb_suggest = request.POST.get("perm_mmsdb_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_mmsdb_suggest)
    perm_mmsdb_description = request.POST.get("perm_mmsdb_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_mmsdb_description)
    perm_sendmms_suggest = request.POST.get("perm_sendmms_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_sendmms_suggest)
    perm_sendmms_description = request.POST.get("perm_sendmms_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_sendmms_description)
    perm_mobileconnectivity_suggest = request.POST.get("perm_mobileconnectivity_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_mobileconnectivity_suggest)
    perm_mobileconnectivity_description = request.POST.get("perm_mobileconnectivity_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_mobileconnectivity_description)
    perm_wificonnectivity_suggest = request.POST.get("perm_wificonnectivity_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_wificonnectivity_suggest)
    perm_wificonnectivity_description = request.POST.get("perm_wificonnectivity_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_wificonnectivity_description)
    perm_btconnectivity_suggest = request.POST.get("perm_btconnectivity_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_btconnectivity_suggest)
    perm_btconnectivity_description = request.POST.get("perm_btconnectivity_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_btconnectivity_description)
    perm_packageinfo_suggest = request.POST.get("perm_packageinfo_suggest", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_packageinfo_suggest)
    perm_packageinfo_description = request.POST.get("perm_packageinfo_description", Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).perm_packageinfo_description)
    comments = request.POST.get('comments', Suggest.objects.get(assign_to=assign_to,version_code=version,package_name=package_name).comments)
   
    Suggest.objects.filter(assign_to=assign_to,version_code=version,package_name=package_name).update(perm_sendsms_suggest=perm_sendsms_suggest,perm_sendsms_description=perm_sendsms_description,perm_callphone_suggest=perm_callphone_suggest,perm_callphone_description=perm_callphone_description,perm_smsdb_suggest=perm_smsdb_suggest,perm_smsdb_description=perm_smsdb_description,perm_contact_suggest=perm_contact_suggest,perm_contact_description=perm_contact_description,perm_calllog_suggest=perm_calllog_suggest,perm_calllog_description=perm_calllog_description,perm_location_suggest=perm_location_suggest,perm_location_description=perm_location_description,perm_phoneinfo_suggest=perm_phoneinfo_suggest,perm_phoneinfo_description=perm_phoneinfo_description,perm_netdefault_suggest=perm_netdefault_suggest,perm_netdefault_description=perm_netdefault_description,perm_netwifi_suggest=perm_netwifi_suggest,perm_netwifi_description=perm_netwifi_description,perm_root_suggest=perm_root_suggest,perm_root_description=perm_root_description,perm_callstate_suggest=perm_callstate_suggest,perm_callstate_description=perm_callstate_description,perm_callmonitor_suggest=perm_callmonitor_suggest,perm_callmonitor_description=perm_callmonitor_description,perm_recorder_suggest=perm_recorder_suggest,perm_recorder_description=perm_recorder_description,perm_settings_suggest=perm_settings_suggest,perm_settings_description=perm_settings_description,perm_autostart_suggest=perm_autostart_suggest,perm_autostart_description=perm_autostart_description,perm_notification_suggest=perm_notification_suggest,perm_notification_description=perm_notification_description,perm_installpackage_suggest=perm_installpackage_suggest,perm_installpackage_description=perm_installpackage_description,perm_audiorecorder_suggest=perm_audiorecorder_suggest,perm_audiorecorder_description=perm_audiorecorder_description,perm_mmsdb_suggest=perm_mmsdb_suggest,perm_mmsdb_description=perm_mmsdb_description,perm_sendmms_suggest=perm_sendmms_suggest,perm_sendmms_description=perm_sendmms_description,perm_mobileconnectivity_suggest=perm_mobileconnectivity_suggest,perm_mobileconnectivity_description=perm_mobileconnectivity_description,perm_wificonnectivity_suggest=perm_wificonnectivity_suggest,perm_wificonnectivity_description=perm_wificonnectivity_description,perm_btconnectivity_suggest=perm_btconnectivity_suggest,perm_btconnectivity_description=perm_btconnectivity_description,perm_packageinfo_suggest=perm_packageinfo_suggest,perm_packageinfo_description=perm_packageinfo_description,finished=finished,update_time=update_time,comments=comments)

    result = '%s %s %s %s 已保存!' % (assign_to, title, version, package_name)
  
    response.write(result)
    return response

@csrf_exempt
@login_required
def is_approved(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    assign_to = request.POST.get('assign_to')
    title = request.POST.get('title')
    version = request.POST.get('version')
    package_name = request.POST.get('package_name')

    Suggest.objects.filter(assign_to=assign_to,
            version_code=version, package_name=package_name).update(approved=1)
    
    result = '%s %s %s %s 已通过!' % (assign_to, title, version, package_name)
    response.write(result)
    return response

@csrf_exempt
@login_required
def not_approved(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    assign_to = request.POST.get('assign_to')
    title = request.POST.get('title')
    version = request.POST.get('version')
    package_name = request.POST.get('package_name')

    Suggest.objects.filter(assign_to=assign_to,
            version_code=version, package_name=package_name).update(approved=0)
    
    result = '%s %s %s %s 未通过!' % (assign_to, title, version, package_name)
    response.write(result)
    return response

@csrf_exempt
@login_required
def is_pending(request):
    """
    给权限添加描述
    """
    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    assign_to = request.POST.get('assign_to')
    title = request.POST.get('title')
    version = request.POST.get('version')
    package_name = request.POST.get('package_name')

    Suggest.objects.filter(assign_to=assign_to,
            version_code=version, package_name=package_name).update(approved=2)
    
    result = '%s %s %s %s 待定!' % (assign_to, title, version, package_name)
    response.write(result)
    return response

@csrf_exempt
@login_required
def downloadApk(request):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
 
    assign_to = request.GET.get('assign_to')
    #category = request.GET.get('category')
    title = request.GET.get('title')
    version = request.GET.get('version')
    package_name = request.GET.get('package_name')

    suggest_list = Suggest.objects.get(title=title, assign_to=assign_to, version_code=version, package_name=package_name)
   
    package_name = suggest_list.package_name
    category = suggest_list.category
    version_code = suggest_list.version_code

    #try:
    if 1==1:
    	fileName = '%s_&_%s_&_%s.apk' % (str(title), str(package_name), str(version_code))
    	f = open(os.path.join(BASE_DIR, 'androguard/download/%s' % fileName))
    	response = HttpResponse(FileWrapper(f), content_type='text/plain')
    	response['Content-Disposition'] = 'attachment; filename=%s' % (fileName).replace(' ', '_').replace(':', '_')
    	return response
    #except:
	fileName = '%s_%s_%s.apk' % (str(title), str(package_name), str(version_code))
    	f = open(os.path.join(BASE_DIR, 'androguard/download/old/%s/%s' % (category.encode('utf8'), fileName)))
     	response = HttpResponse(FileWrapper(f), content_type='text/plain')
    	response['Content-Disposition'] = 'attachment; filename=%s' % (fileName).replace(' ', '_')
    	return response

@csrf_exempt
@login_required
def checkApk(request):

    response=HttpResponse()  
    response['Content-Type'] = 'text/string'

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
 
    assign_to = request.POST.get('assign_to')
    title = request.POST.get('title')
    version = request.POST.get('version')
    package_name = request.POST.get('package_name')

    perms = Suggest.objects.get(assign_to=assign_to, version_code=version, package_name=package_name)

    packageName = perms.package_name
    title = perms.title
    md5 = perms.md5

    try:
        versionCode, downloadUrl = checkVersion(packageName)
        if float(version) >= float(versionCode):
            result = '没有新版本更新。now: %s, last: %s' % (str(versionCode), str(version))
        else:
            result = '请等待后台更新版本。now: %s, last: %s' % (str(versionCode), str(version))
            #subprocess.Popen()
        response.write(result)
        return response
    except:
        result = 'versionCode: %s, packageName: %s, title: %s' % (str(version), str(packageName), str(title))
        log.debug(result)
        return response
