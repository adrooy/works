#coding=utf-8


__author__ = 'xiangxiaowei'


from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from forms import LoginForm


@csrf_protect
def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()    
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            _login(request,form.cleaned_data['username'],form.cleaned_data['password'])
            return HttpResponseRedirect(reverse('sdcleaner index'))
            #return render_to_response('accounts/login.html', template_var, context_instance=RequestContext(request))
    template_var['form']=form        
    return render_to_response('accounts/login.html', template_var, context_instance=RequestContext(request))
    
def _login(request,username,password):
    '''登陆核心方法'''
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth_login(request, user)
            request.session['username'] = username
            ret = True
    else:
        messages.add_message(request, messages.INFO, _(u'请正确输入账号和密码'))
        return ret
    
@csrf_protect
def logout(request):
    '''注销视图'''
    auth_logout(request)
    return HttpResponseRedirect(reverse('sdcleaner index'))
