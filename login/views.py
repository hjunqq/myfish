# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.template import RequestContext,Template
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseBadRequest
from django.db.models import Q
from django.utils import timezone 

import datetime
import calendar
import pytz
import json

from .models import *
from .forms import *
from user_agents import parse


@login_required
def home_page(request):
    """Home Page"""
    """    if not request.user.is_authenticated():
            response = HttpResponseRedirect('/login/')
            return response  """   
    return HttpResponseRedirect('/daily')

def login_page(request):
    """Login Page"""
    dailymsg = "Many persons have a wrong idea of what constitutes true happiness. It is not attained through self-gratification but through fidelity to a worthy purpose. —Helen Keller"   
    if request.method == "GET":
        redirect_to =request.GET.get('next', '/') 
        if request.user.is_authenticated():
            response = HttpResponseRedirect(redirect_to)
            return response        
    elif request.method == 'POST':
        uf = UserForm(request.POST)       
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            remmember_me = uf.cleaned_data['remember_me']
            redirect_to =request.POST.get('next', '/') 
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                if remmember_me:
                    request.session.set_expiry(1209600)     # 2 weeks
                else:
                    request.session.set_expiry(0)           # on closed
                if request.META.has_key('HTTP_CF_CONNECTING_IP'):
                    logInIP = request.META['HTTP_CF_CONNECTING_IP']
                else:
                    logInIP = request.META['REMOTE_ADDR']
                logInTime = timezone.now()
                logOutTime = timezone.now()
                UserAgent = str(parse(request.META.get('HTTP_USER_AGENT')))
                try:
                    UItem= UserLogInfo.objects.create(user = user,
                                                      logInIP = logInIP,
                                                      logInTime = logInTime,
                                                      logOutTime = logOutTime, 
                                                      UserAgent = UserAgent)
                except:
                    pass                
                if request.is_ajax:            
                    return HttpResponse(json.dumps(redirect_to),content_type="application/json") 
                else:
                    return HttpResponseRedirect(redirect_to)
            else:
                if request.is_ajax: 
                    error = r"错误用户名或密码"
                    return HttpResponseBadRequest(
                        json.dumps(error),content_type="application/json"
                    )                
        else:
            uf = UserForm()
    else:
        uf = UserForm()
    return render_to_response('login_page.html',locals(),context_instance=RequestContext(request))


def logout_page(request):
    """Logout Page"""
    try :
        user = request.user
        userItem = UserLogInfo.objects.get(user=user)
        userItem.logOutData = timezone.now()
        userItem.save()
    except:
        pass
    logout(request)
    return HttpResponseRedirect('/login/')

