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

import urllib,urllib2
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
from cStringIO import StringIO

import calendar
import pytz
import json
import datetime

from .models import *
from .forms import *

def get_bing_dailysens():
    """获得bing每日一句"""
    url = "http://cn.bing.com/dict/clienthomepagev2"
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, "html.parser")
    dailysens = soup.find_all("div",class_="client_daily_sens_bar")[0]
    dailysens_en = dailysens.find_all("div",class_="client_daily_text_en")[0]
    dailysens_cn = dailysens.find_all("div",class_="client_daily_text_zh")[0]
    dailysens_en_text,dailysens_author = dailysens_en.text.split(u"\u2014")
    dailysens_cn_text = dailysens_cn.text    
    content.close() 
    return dailysens_en_text,dailysens_cn_text,dailysens_author

def get_bing_wallpaper():
    idx = '0'
    url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=' + idx + '&n=1&mkt=zh-CN'
    #ru-RU, because they always have 1920x1200 resolution pictures
    #url = "http://www.bing.com/?mkt=zh-CN"
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, "html.parser")
    
    picurl = soup.find_all("url")[0]
    url = 'http://www.bing.com' + picurl.string
    #now = datetime.datetime.now()
    #picPath = now.strftime('BingWallpaper-%Y-%m-%d') + '.jpg'
    #img_temp = NamedTemporaryFile(delete=True)
    #img_temp.write(urllib.urlretrieve(url.replace('_1366x768', '_1920x1200'), picPath))
    #img_temp.flush()
    #if not os.path.isfile(picPath):
        #urllib.urlretrieve(url.replace('_1366x768', '_1920x1200'), picPath)
        ##urllib.urlretrieve(url, picPath)
    #else:
        #print "File exists."
    content.close() 
    return url.replace('_1366x768', '_1920x1200')

def get_Additivity(user,date):
    """判断可添加性"""
    try:
        today = DailyContent.objects.get(user=user,date=date)
        Additivity = False
    except DailyContent.DoesNotExist:
        Additivity = True
    return Additivity
def get_commentstat(date):
    if date < timezone.localtime(timezone.now()).date():
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
    prev_set = DailyContent.objects.filter(date__lt=date).order_by('-date')
    if prev_set:
        prev_date = prev_set[0].date
    else:
        prev_date = date
    return prev_date
    

@login_required
def add_new(request):
    """add new home"""
    user = request.user
    date = timezone.localtime(timezone.now()).date()
    addtivity = get_Additivity(user, date)
    dailysens_en,dailysens_cn,dailysens_author = get_bing_dailysens()
    dailypic = get_bing_wallpaper()
    if request.method == "POST":
        form = AddForm(request.POST,request.FILES)
        if form.is_valid():
            img = form.cleaned_data['mainimage'] 
            url = form.cleaned_data['mainimageurl']
            sentence = form.cleaned_data['sentence']
            author = form.cleaned_data['author']
            try:
                dailycontent = DailyContent.objects.get_or_create(user = user,
                                                                  date = date)[0]
                if img:
                    dailycontent.img = img
                if url:
                    picPath = date.strftime('BingWallpaper-%Y-%m-%d') + '.jpg'
                    s = StringIO()
                    s.write(urllib2.urlopen(url).read())
                    dailycontent.img.save(picPath,File(s),save=True)
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
    date = timezone.localtime(timezone.now()).date()
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
    date = timezone.localtime(timezone.now()).date()
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
