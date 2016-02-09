from django.db.models import Q
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse,reverse_lazy

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.template import RequestContext,Template
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseBadRequest
from django.utils import timezone 
from django.core import serializers
from django.http import JsonResponse

import calendar
import pytz
import json
import datetime


from . import models
from . import forms

class EntriesList(ListView):

    model = models.Entry
    template_name = 'andablog/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super(EntriesList, self).get_queryset().filter(
            Q(is_published=True) | Q(author__isnull=False, author=self.request.user.id))
        return queryset.order_by('is_published', '-published_timestamp')  # Put 'drafts' first.


class EntryDetail(DetailView):

    model = models.Entry
    template_name = 'andablog/entry_detail.html'
    context_object_name = 'entry'
    slug_field = 'slug'

    def get_queryset(self):
        return super(EntryDetail, self).get_queryset().filter(
            Q(is_published=True) | Q(author__isnull=False, author=self.request.user.id))

class EntriesListUnpublished(ListView):
    model = models.Entry
    template_name = 'andablog/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10
    paginate_orphans = 5    
    
    def get_queryset(self):
        queryset = super(EntriesListUnpublished, self).get_queryset().filter(
            Q(is_published=False) | Q(author__isnull=False, author=self.request.user.id))
        return queryset.order_by('is_published', '-published_timestamp')  # Put 'drafts' first.    

class EntryDetailUnpublished(DetailView):

    model = models.Entry
    template_name = 'andablog/entry_detail.html'
    context_object_name = 'entry'
    slug_field = 'slug'

    def get_queryset(self):
        return super(EntryDetailUnpublished, self).get_queryset().filter(
            Q(is_published=False) | Q(author__isnull=False, author=self.request.user.id))

class EntryCreate(CreateView):
    model = models.Entry
    template_name = 'andablog/entry_create.html'
    fields = ['title','content','is_published','tags']
    context_object_name = 'entry'
    
    def get_success_url(self):
        slug=self.object.slug
        if self.object.is_published:
            return reverse('andablog:entrydetail',args=[slug])
        else:
            return reverse('andablog:entrydetailunpublished',args=[slug])
    
    def get_success_url(self):
        slug=self.object.slug
        if self.object.is_published:
            return reverse('andablog:entrydetail',args=[slug])
        else:
            return reverse('andablog:entrydetailunpublished',args=[slug])
    
    def get_success_url(self):
        slug=self.object.slug
        if self.object.is_published:
            return reverse('andablog:entrydetail',args=[slug])
        else:
            return reverse('andablog:entrydetailunpublished',args=[slug])
    
      

class EntryUpdate(UpdateView):
    model = models.Entry
    template_name_suffix = '_update'
    context_object_name = 'entry'
    fields = ['title','content','is_published','tags']
    
    def get(self, request,**kwargs):
        self.object = models.Entry.objects.get(slug=self.kwargs['slug'])
        context = self.get_context_data(object = self.object)
        return self.render_to_response(context)
 
    def get_success_url(self):
        slug=self.object.slug
        if self.object.is_published:
            return reverse('andablog:entrydetail',args=[slug])
        else:
            return reverse('andablog:entrydetailunpublished',args=[slug])
        

class EntryDelete(DeleteView):
    model = models.Entry
    success_url = '/blog/'
    template_name_suffix = '_delete'
    context_object_name = 'entry'
    
    def get_object(self, *args, **kwargs):
        return models.Entry.objects.get(slug=self.kwargs['slug'])
    
    
@login_required
def EntryAdd(request):
    return HttpResponseRedirect('/admin/andablog/entry/add/')
    user = request.user
    form = forms.AddPost()
    if request.method == 'GET':
        return render_to_response('andablog/entry_add.html',locals(),context_instance=RequestContext(request)) 
        