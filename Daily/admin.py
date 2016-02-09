from django.contrib import admin

# Register your models here.

from .models import *

class DailyContentList(admin.ModelAdmin):
    list_display = ('pk','user','date')

admin.site.register(DailyContent,DailyContentList)
