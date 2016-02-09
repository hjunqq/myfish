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
from django.core import serializers
from django.http import JsonResponse

import calendar
import pytz
import json
import datetime

from .models import *
from .forms import *

def get_Additivity(user,date):
    """判断可加性"""
    try:
        today = DailyContent.objects.get(user=user,date=date)
        Additivity = False
    except DailyContent.DoesNotExist:
        Additivity = True
    return Additivity
def get_commentstat(date):
    if date < timezone.now().date():
        commentability = False
    else:
        commentability = True
    return commentability

def get_daily_content(date):
    """获得今天状态"""
    multidaily = False
    try:
        dailycontent = DailyContent.objects.filter(date=date)
    except:
        dailycontent = []
    return dailycontent

def get_daily_content_by_pk(pk):
    """by Pk"""
    try:
        icontent = DailyContent.objects.get(pk=pk)
    except:
        pass
    return icontent  

def get_next_date(date):
    next_set = DailyContent.objects.filter(date__gt=date)
    if next_set:
        next_date=next_set[0].date
    else:
        next_date=date
    return next_date

def get_prev_date(date):
    prev_set = DailyContent.objects.filter(date__lt=date)
    if prev_set:
        prev_date = prev_set[0].date
    else:
        prev_date = date
    return prev_date
    

@login_required
def add_new(request):
    """add new home"""
    user = request.user
    date = timezone.now().date()
    addtivity = get_Additivity(user, date)
    if request.method == "POST":
        form = AddForm(request.POST,request.FILES)
        if form.is_valid():
            img = form.cleaned_data['mainimage'] 
            sentence = form.cleaned_data['sentence']
            author = form.cleaned_data['author']
            try:
                dailycontent = DailyContent.objects.get_or_create(user = user,
                                                                  date = date)[0]
                dailycontent.img = img
                dailycontent.sentence = sentence
                dailycontent.author = author
                dailycontent.save()
                msg = 'submit success'
            except:
                msg = 'submit failed'
                pass
            return HttpResponse(json.dumps(msg), content_type="application/json")
        else:
            form = AddForm()
    else:
        form = AddForm()
    return render_to_response('add_new.html',locals(),context_instance=RequestContext(request)) 

@login_required
def daily_page(request):
    """Home Page"""
    """    if not request.user.is_authenticated():
            response = HttpResponseRedirect('/login/')
            return response  """   
    user = request.user
    date = timezone.now().date()
    additivity = get_Additivity(user, date)    
    dailycontent = get_daily_content(date)
    prev_date = get_prev_date(date)
    next_date = get_next_date(date)
    commentability = get_commentstat(date)
    return render_to_response('daily_home.html',locals(),context_instance=RequestContext(request))

@login_required
def daily_page_json(request):
    """daily_page_json"""
    user = request.user
    date = timezone.now().date()
    if request.method == "POST":
        formtype = request.POST['formtype']
        if formtype == 'like':
            form = LikeForm(request.POST)
            if form.is_valid():
                likeId = form.cleaned_data['liked_item']
                try:
                    icontent = DailyContent.objects.get(pk=likeId,likedby=user)
                    icontent.likedby.remove(user)
                    icontent.save()
                except DailyContent.DoesNotExist:
                    icontent = DailyContent.objects.get(pk=likeId)
                    icontent.likedby.add(user)
                    icontent.save()
                icontent = get_daily_content_by_pk(pk=likeId)
                print icontent.likedby.count()
                return render_to_response('daily_like.html',locals(),context_instance=RequestContext(request))
        elif formtype  =='reloadcomment':
            icontent_id = request.POST['icontent_id']
            icontent = get_daily_content_by_pk(pk=icontent_id)
            return render_to_response('daily_comment.html',locals(),context_instance=RequestContext(request))
    msg = 'GET'
    return JsonResponse(json.dumps(msg),safe=False)

@login_required
def specific_day(request,date):
    user = request.user
    try:
        date = datetime.datetime.strptime(date,"%Y%m%d").date()
        dailycontent = get_daily_content(date)
        if dailycontent.count() == 0:
            page_msg = "今天没有内容！"        
    except ValueError:
        page_msg = "日期错误！"
        dailycontent = []
    additivity = False
    prev_date = get_prev_date(date)
    next_date = get_next_date(date)    
    commentability = get_commentstat(date)
    return render_to_response('daily_home.html',locals(),context_instance=RequestContext(request))
