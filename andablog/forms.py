from django import forms

from django.views.generic.edit import CreateView
from .models import *
from markitup.widgets import MarkItUpWidget
from taggit.forms import *

class AddPost(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=MarkItUpWidget())
    is_published = forms.BooleanField()
    tags = TagField()    
